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

# all bins in a subchannel / channel
def make_workspace_bins(dim, channel, version, datacard_dict, WCs, ScanType, verbose=1, StatOnly=False):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    print('Channel: %s' % channel)
    for i, subch in enumerate(subchannels):
        print('Subchannel: "%s"' % subch)
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
        # loop through bins
        bins = datacard_dict[channel]['subchannels'][subch]['bins']
        for bin_n in bins:
            print('bin%s' % bin_n)
            sname_sch_b = sname_sch + '_bin' + str(bin_n)
            cmd_str = 'text2workspace.py '
            tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
            # TEST
            print(tfile)
            dc_file = os.path.join(dcdir, channel, version, tfile)
            cmd_str += '%s %s ' % (dc_file, str_module)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
            wsfile = os.path.join(dcdir, 'workspaces', 'single_bin', wsfile)
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
    if verbose > 0:
        print('\n%s done.\n\n' % channel)

# all subchannels in a channel
def make_workspace_subchannels(dim, channel, version, datacard_dict, WCs, ScanType, verbose=1, StatOnly=False, SignalInject=False, WC=None):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    print('Channel: %s' % channel)
    for i, subch in enumerate(subchannels):
        cmd_str = 'text2workspace.py '
        print('Subchannel: %s' % subch)
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
        tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
        if SignalInject:
            dc_file = os.path.join(dcdir, channel, version, 'signal_injection_'+WC, tfile)
        else:
            dc_file = os.path.join(dcdir, channel, version, tfile)
        cmd_str += '%s %s ' % (dc_file, str_module)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(dcdir, 'workspaces', 'subchannel', wsfile)
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
    if verbose > 0:
        print('\n%s done.\n\n' % channel)
    else:
        print()

# all channels
def make_workspace_channels(dim, channels, datacard_dict, WCs, ScanType, verbose=1, StatOnly=False, SignalInject=False, WC=None):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'channel')
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    # channels = datacard_dict.keys()
    for i, ch in enumerate(channels):
        # WCs = versions_dict[ch]['EFT_ops']
        # if not WC in WCs:
        #     continue
        print('Channel: %s' % ch)
        cmd_str = 'text2workspace.py '
        v = versions_dict[ch]['v']
        version = 'v'+str(v)
        sname_ch = datacard_dict[ch]['info']['short_name']
        tfile_ch = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version=version, file_type='txt')
        dc_file = os.path.join(dcdir, tfile_ch)
        cmd_str += '%s %s ' % (dc_file, str_module)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(datacard_dir, 'workspaces', 'channel', wsfile)
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
    if verbose > 0:
        print('\nall channels done.\n\n')

# full analysis
def make_workspace_full_analysis(dim, WCs, ScanType, verbose=1, StatOnly=False, SignalInject=False, WC=None):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis')
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined', WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    dc_file = os.path.join(dcdir, tfile_comb)
    print('Full Analysis')
    cmd_str = 'text2workspace.py '
    cmd_str += '%s %s ' % (dc_file, str_module)
    wsfile = template_filename.substitute(channel='all', subchannel='_combined', WC=dim, ScanType=ScanType, purpose='workspace'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='root')
    wsfile = os.path.join(datacard_dir, 'workspaces', 'full_analysis', wsfile)
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
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run make workspaces for? "all" (default). Any combination in any order of the following characters will work: "b" (bin), "s" (subchannel), "c" (channel), "f" (full analysis). e.g. "bsc" will run all but the full analysis.')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study in the signal injection case? ["cW" (default), ...]')
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
    if (args.theLevels is None) or (args.theLevels == 'all'):
        generate_bins = True
        generate_subch = True
        generate_ch = True
        generate_full = True
    else:
        if 'b' in args.theLevels:
            generate_bins = True
        else:
            generate_bins = False
        if 's' in args.theLevels:
            generate_subch = True
        else:
            generate_subch = False
        if 'c' in args.theLevels:
            generate_ch = True
        else:
            generate_ch = False
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    # cannot do bin level with signal injection
    if SignalInject:
        generate_bins = False
    # else:
    #     generate_bins = True
    if args.WC is None:
        args.WC = 'cW'
    if args.Verbose is None:
        args.Verbose = 1
    else:
        args.Verbose = int(args.Verbose)
    # check if dim6 and dim8 in WC_ALL
    # dims = set()
    dims = ['dim6', 'dim8']
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
    # dims = list(dims)
    #########################
    # outer loop (over EFT dimension)
    for dim, WCs in zip(dims, [WCs_dim6, WCs_dim8]):
        print(dim)
        if len(WCs) < 1:
            print('No WC in WC_ALL with dim %s! Skipping...' % dim)
            continue
        print('=================================================')
        #########################
        # bins workspaces
        if generate_bins:
            print('Generating bin workspaces:')
            print('=================================================')
            for channel in channels:
                # WCs = versions_dict[channel]['EFT_ops']
                # if not WC in WCs:
                #     continue
                v = versions_dict[channel]['v']
                VERSION = 'v'+str(v)
                print(channel, VERSION)
                for StatOnly in [False, True]:
                    print('Stat only? ', StatOnly)
                    make_workspace_bins(dim, channel, VERSION, datacard_dict, WCs=WCs, ScanType=args.ScanType, verbose=args.Verbose, StatOnly=StatOnly)
            print('=================================================\n')
        #########################
        # subchannel workspaces
        if generate_subch:
            print('Generating subchannel workspaces:')
            print('=================================================')
            for channel in channels:
                # WCs = versions_dict[channel]['EFT_ops']
                # if not WC in WCs:
                #     continue
                v = versions_dict[channel]['v']
                VERSION = 'v'+str(v)
                for StatOnly in [False, True]:
                    print('Stat only? ', StatOnly)
                    make_workspace_subchannels(dim, channel, VERSION, datacard_dict, WCs=WCs, ScanType=args.ScanType, verbose=args.Verbose, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC)
            print('=================================================\n')
        #########################
        # channel workspaces
        if generate_ch:
            print('Generating channel workspaces:')
            print('=================================================')
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                make_workspace_channels(dim, channels, datacard_dict, WCs=WCs, ScanType=args.ScanType, verbose=args.Verbose, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC)
            print('=================================================\n')
        #########################
        # full analysis workspace
        if generate_full:
            print('Generating full analysis workspace:')
            print('=================================================')
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                make_workspace_full_analysis(dim, WCs=WCs, ScanType=args.ScanType, verbose=args.Verbose, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC)
            print('=================================================\n')
        #########################
