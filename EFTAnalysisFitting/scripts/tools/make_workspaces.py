'''
Makes all workspaces at the bin-by-bin, subchannel, channel, full analysis levels.
To make sure up to date datacards and ROOT yield files are used, please ensure
scripts/tools/combine_cards.py and scripts/tools/split_yields.py(or run_split_yields.sh) have both been
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
from CONFIG_VERSIONS import versions_dict
from MISC_CONFIGS import template_filename, datacard_dir

str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
x_flag = '--X-allow-no-signal'

# all bins in a subchannel / channel
def make_workspace_bins(channel, version, datacard_dict, WC, ScanType, verbose=1):
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    print(f'Channel: {channel}')
    for i, subch in enumerate(subchannels):
        print(f'Subchannel: {subch}', end=': ')
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        # loop through bins
        bins = datacard_dict[channel]['subchannels'][subch]['bins']
        for bin_n in bins:
            print(f'bin{bin_n}, ', end='')
            sname_sch_b = sname_sch + f'_bin{bin_n}'
            cmd_str = 'text2workspace.py '
            tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
            dc_file = os.path.join(dcdir, channel, version, tfile)
            cmd_str += f'{dc_file} {str_module} '
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType, purpose='workspace', proc='', version=version, file_type='root')
            wsfile = os.path.join(dcdir, 'workspaces', 'single_bin', wsfile)
            cmd_str += f'-o {wsfile} {x_flag} '
            # add correct WC
            cmd_str += f'--PO eftOperators={WC}'
            # run script
            if verbose > 0:
                stdout = None
            else:
                stdout = subprocess.PIPE
            if verbose > 0:
                print('generating workspace...')
            _ = subprocess.run(cmd_str, shell=True, stdout=stdout)
            if verbose > 0:
                print('\ndone.\n')
    if verbose > 0:
        print(f'\n{channel} done.\n\n')
    else:
        print()

# all subchannels in a channel
def make_workspace_subchannels(channel, version, datacard_dict, WC, ScanType, verbose=1):
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    # print(f'Channel: {channel}; Subchannel: ', end='')
    print(f'Channel: {channel}')
    for i, subch in enumerate(subchannels):
        cmd_str = 'text2workspace.py '
        print(f'Subchannel: {subch}', end=': ')
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
        dc_file = os.path.join(dcdir, channel, version, tfile)
        cmd_str += f'{dc_file} {str_module} '
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc='', version=version, file_type='root')
        wsfile = os.path.join(dcdir, 'workspaces', 'subchannel', wsfile)
        cmd_str += f'-o {wsfile} {x_flag} '
        # add correct WC
        cmd_str += f'--PO eftOperators={WC}'
        # run script
        if verbose > 0:
            stdout = None
        else:
            stdout = subprocess.PIPE
        if verbose > 0:
            print('generating workspace...')
        _ = subprocess.run(cmd_str, shell=True, stdout=stdout)
        if verbose > 0:
            print('\ndone.\n')
    if verbose > 0:
        print(f'\n{channel} done.\n\n')
    else:
        print()

# all channels
def make_workspace_channels(datacard_dict, WC, ScanType, verbose=1):
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'channel')
    channels = datacard_dict.keys()
    for i, ch in enumerate(channels):
        print(f'Channel: {ch}', end=': ')
        cmd_str = 'text2workspace.py '
        v = versions_dict[ch]['v']
        version = f'v{v}'
        sname_ch = datacard_dict[ch]['info']['short_name']
        tfile_ch = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
        dc_file = os.path.join(dcdir, tfile_ch)
        cmd_str += f'{dc_file} {str_module} '
        wsfile = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType, purpose='workspace', proc='', version=version, file_type='root')
        wsfile = os.path.join(datacard_dir, 'workspaces', 'channel', wsfile)
        cmd_str += f'-o {wsfile} {x_flag} '
        # add correct WC
        cmd_str += f'--PO eftOperators={WC}'
        # run script
        if verbose > 0:
            stdout = None
        else:
            stdout = subprocess.PIPE
        if verbose > 0:
            print('generating workspace...')
        _ = subprocess.run(cmd_str, shell=True, stdout=stdout)
        if verbose > 0:
            print('\ndone.\n')
    if verbose > 0:
        print(f'\nall channels done.\n\n')
    else:
        print()

# full analysis
def make_workspace_full_analysis(WC, ScanType, verbose=1):
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis')
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined', WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version='vCONFIG_VERSIONS', file_type='txt')
    dc_file = os.path.join(dcdir, tfile_comb)
    # print(dc_file)
    print('Full Analysis', end=': ')
    cmd_str = 'text2workspace.py '
    cmd_str += f'{dc_file} {str_module} '
    wsfile = template_filename.substitute(channel='all', subchannel='_combined', WC=WC, ScanType=ScanType, purpose='workspace', proc='', version='vCONFIG_VERSIONS', file_type='root')
    wsfile = os.path.join(datacard_dir, 'workspaces', 'full_analysis', wsfile)
    # print(wsfile)
    cmd_str += f'-o {wsfile} {x_flag} '
    # add correct WC
    cmd_str += f'--PO eftOperators={WC}'
    # run script
    if verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    if verbose > 0:
        print('generating workspace...')
    _ = subprocess.run(cmd_str, shell=True, stdout=stdout)
    if verbose > 0:
        print('\ndone.\n')
    else:
        print()


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default),]')
    parser.add_argument('-s', '--ScanType',
                        help=f'What type of EFT scan was included in this file? ["_1D" (default),]')
    parser.add_argument('-V', '--Verbose',
                        help=f'Include "combine" output? 0 / 1 (default). "combine" output included if Verbose>0.')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'cW'
    if args.ScanType is None:
        args.ScanType = '_1D'
    if args.Verbose is None:
        args.Verbose = 1
    else:
        args.Verbose = int(args.Verbose)
    #########################
    # bins workspaces
    print('Generating bin workspaces:')
    print('=================================================')
    for channel in datacard_dict.keys():
        v = versions_dict[channel]['v']
        VERSION = f'v{v}'
        make_workspace_bins(channel, VERSION, datacard_dict, WC=args.WC, ScanType=args.ScanType, verbose=args.Verbose)
    print('=================================================\n')
    '''
    #########################
    # subchannel workspaces
    print('Generating subchannel workspaces:')
    print('=================================================')
    for channel in datacard_dict.keys():
        v = versions_dict[channel]['v']
        VERSION = f'v{v}'
        make_workspace_subchannels(channel, VERSION, datacard_dict, WC=args.WC, ScanType=args.ScanType, verbose=args.Verbose)
    print('=================================================\n')
    #########################
    # channel workspaces
    print('Generating channel workspaces:')
    print('=================================================')
    make_workspace_channels(datacard_dict, WC=args.WC, ScanType=args.ScanType, verbose=args.Verbose)
    print('=================================================\n')
    #########################
    # full analysis workspace
    print('Generating full analysis workspace:')
    print('=================================================')
    make_workspace_full_analysis(WC=args.WC, ScanType=args.ScanType, verbose=args.Verbose)
    print('=================================================\n')
    #########################
    '''
