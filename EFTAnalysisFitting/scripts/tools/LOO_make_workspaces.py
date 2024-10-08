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
def make_workspace_full_analysis_leave_one_out(channel_leave_out, dim, WCs, ScanType, verbose=1, StatOnly=False, SignalInject=False, WC=None):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'leave_one_out')
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+channel_leave_out, WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    dc_file = os.path.join(dcdir, tfile_comb)
    print('Full Analysis')
    cmd_str = 'text2workspace.py '
    cmd_str += '%s %s ' % (dc_file, str_module)
    wsfile = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+channel_leave_out, WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='root')
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
                        help='Which channel to leave out? ["all" (default, looping), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-d', '--Dimension',
                        help='Which dim of EFT ops to process? "all" (default), "dim6", "dim8"')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    parser.add_argument('-V', '--Verbose',
                        help='Include "combine" output? 0 / 1 (default). "combine" output included if Verbose>0.')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
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
            print('Leaving out: %s' % channel)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                make_workspace_full_analysis_leave_one_out(channel, dim, WCs=WCs, ScanType=args.ScanType, verbose=args.Verbose, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC)
        print('=================================================\n')
        #########################
