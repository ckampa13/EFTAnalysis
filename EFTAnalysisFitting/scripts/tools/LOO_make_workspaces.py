'''
Makes all workspaces at the bin-by-bin, subchannel, channel, full analysis levels.
To make sure up to date datacards and ROOT yield files are used, please ensure
scripts/tools/combine_cards.py and scripts/tools/split_yields.py have both been
run.

In the current version, only single WC are supported.
'''
import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename, datacard_dir, dim6_ops

str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
x_flag = '--X-allow-no-signal'

# full analysis
def make_workspace_full_analysis_leave_one_out(channels_leave_out, dim, WCs, ScanType, verbose=1, StatOnly=False, SignalInject=False, WC=None, file_suff=None, vsuff=''):
    if file_suff is None:
        file_suff = channels_leave_out[0]
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'leave_one_out')
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    # tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+channel_leave_out, WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+file_suff, WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='txt')
    dc_file = os.path.join(dcdir, tfile_comb)
    print('Full Analysis')
    cmd_str = 'text2workspace.py '
    cmd_str += '%s %s ' % (dc_file, str_module)
    # wsfile = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+channel_leave_out, WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='root')
    wsfile = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+file_suff, WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='root')
    wsfile = os.path.join(datacard_dir, 'workspaces', 'leave_one_out', wsfile)
    cmd_str += '-o %s %s ' % (wsfile, x_flag)
    # add correct WCs
    WCs_str = ','.join(WCs)
    cmd_str += '--PO eftOperators=%s' % WCs_str
    # run script
    if verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    if verbose > 0:
        print('generating workspace...')
        print(cmd_str)
    _ = subprocess.call(cmd_str, shell=True, stdout=stdout)
    if verbose > 0:
        print('\ndone.\n')
    else:
        print()


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel to leave out? ["all" (default, looping), "all_tau" (remove tau channels), "not_tau" (combine tau channels), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-d', '--Dimension',
                        help='Which dim of EFT ops to process? "all" (default), "dim6", "dim8"')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for NDIM files. ["" (default), "_NDIM",...]')
    parser.add_argument('-V', '--Verbose',
                        help='Include "combine" output? 0 / 1 (default). "combine" output included if Verbose>0.')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()+['all_tau', 'not_tau']
    else:
        channels = [args.Channel]
    if args.Dimension == 'all':
        dims = ['dim6', 'dim8']
    elif args.Dimension == 'dim6':
        dims = ['dim6']
    elif args.Dimension == 'dim8':
        dims = ['dim8']
    else:
        raise ValueError('The input args.Dimension="%s" is not implemented. Please select from: ["all", "dim6", "dim8"].' % args.Dimension)
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    if args.Verbose is None:
        args.Verbose = 1
    else:
        args.Verbose = int(args.Verbose)
    # check if dim6 and dim8 in WC_ALL
    # dims = set()
    #dims = ['dim6', 'dim8']
    WCs_dim6 = []
    WCs_dim8 = []
    for WC in WC_ALL:
        if WC in dim6_ops:
            # dims.add('dim6')
            WCs_dim6.append(WC)
    for WC in WC_ALL:
        if not WC in dim6_ops:
            # dims.add('dim8')
            WCs_dim8.append(WC)
    WCs_dim_dict = {'dim6': WCs_dim6, 'dim8': WCs_dim8}
    # dims = list(dims)
    #########################
    # outer loop (over EFT dimension)
    # for dim, WCs in zip(dims, [WCs_dim6, WCs_dim8]):
    for dim in dims:
        WCs = WCs_dim_dict[dim]
        print(dim)
        if len(WCs) < 1:
            print('No WC in WC_ALL with dim %s! Skipping...' % dim)
            continue
        print('=================================================')
        #########################
        # full analysis workspace
        print('Generating full analysis (leave one out) workspaces:')
        print('=================================================')
        for channel in channels:
            if channel == 'all_tau':
                channels_leave_out = [ch for ch in datacard_dict.keys() if ch[-3:] == '_1T']
                file_suff = 'all_tau'
                print('"all_tau" has the following channels: %s' % channels_leave_out)
            elif channel == 'not_tau':
                channels_leave_out = [ch for ch in datacard_dict.keys() if ch[-3:] != '_1T']
                file_suff = 'not_tau'
                print('"not_tau" has the following channels: %s' % channels_leave_out)
            else:
                channels_leave_out = [channel]
                file_suff = None
            print('Leaving out: %s' % channel)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                make_workspace_full_analysis_leave_one_out(channels_leave_out, dim, WCs=WCs, ScanType=args.ScanType,
                                                           verbose=args.Verbose, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC,
                                                           file_suff=file_suff, vsuff=vsuff)
        print('=================================================\n')
        #########################
