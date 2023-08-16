'''
Generic running of combine for extracting EFT limits. Nominally this is the
"MultiDimFit". Runs the calculation automatically at all levels (bin-by-bin,
subchannel, channel, full analysis) unless otherwise specified in the command
line args. This script runs for a single WC. Doing many WCs can be handled
by writing a bash script.

To make sure up to date datacards, ROOT yield files, and workspaces are used, please ensure
scripts/tools/combine_cards.py, scripts/tools/split_yields.py(or run_split_yields.sh),
and scripts/tools/make_workspaces.py have all been run for the WC of interest.

In the current version, only single WC are supported.
'''
import os
import subprocess
import shutil
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import (
    datacard_dir,
    template_filename,
    template_outfilename,
    template_outfilename_stub,
)

# FIXME! method should be a cmdline arg, but need to make sure it works
METHOD = 'MultiDimFit'

# for finding appropriate scan range
rangescript = os.path.join(datacard_dir, 'scripts', 'tools', 'find_POI_range.py')

# str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
# x_flag = '--X-allow-no-signal'

# utility functions
def find_range(WC, output_file_name, Precision, PrecisionCoarse, Threshold=4.0):
    cmd_str = f'python {rangescript} -f {output_file_name} -w {WC} -T {Threshold} '
    cmd_str += f'-s {Precision} -sc {args.PrecisionCoarse}'
    proc = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE)
    # parse results
    grid_dict = {i.split(':')[0]:float(i.split(':')[1]) for i in proc.stdout.decode().strip('\n').split(';')}
    grid_dict['steps'] = int(grid_dict['steps'])
    print(f'LL: {grid_dict["LL"]}; UL: {grid_dict["UL"]}; steps: {grid_dict["steps"]}')
    range_ = grid_dict["UL"] - grid_dict["LL"]
    # FIXME! I don't think "prec" is used anywhere...
    # also can switch from hard coding the very coarse precision if desired
    if range_ > 50:
        prec = 1.0
        print('Using prec = 1.0')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/1.) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 1.
    elif range_ > 25:
        prec = 0.1
        print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/0.1) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 0.1
    elif range_ > 10:
        prec = args.PrecisionCoarse
        print('Using PrecisionCoarse')
    else:
        prec = args.Precision
        print('Using Precision')
    return grid_dict, prec

def construct_combine_cmd_str(WC, workspace_file, grid_dict, asimov_str,
                              name_str, with_syst=True, method='MultiDimFit'):
    points = grid_dict['steps']
    LL = grid_dict['LL']
    UL = grid_dict['UL']
    cmd_str = f'combine -M {method} {workspace_file} --algo=grid --points {points} '
    cmd_str += f'--alignEdges 1 {asimov_str} --redefineSignalPOIs k_{WC} '
    if with_syst:
        freeze_group = 'nosyst'
    else:
        freeze_group = 'allsyst'
    cmd_str += f'--freezeNuisanceGroups {freeze_group} --freezeParameters r '
    cmd_str += f'--setParameters r=1 --setParameterRanges k_{WC}={LL},{UL} '
    cmd_str += f'--verbose -1 -n {name_str}'
    return cmd_str

# all bins in a subchannel / channel
def run_combine_bins(channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                     Precision, PrecisionCoarse, stdout, verbose=0):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    wsdir = os.path.join(datacard_dir, 'workspaces', 'single_bin')
    outdir = os.path.join(datacard_dir, 'output', 'single_bin')
    os.chdir(outdir)
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
        # for bin_n in ['1']: # TEST
            print(f'bin{bin_n}, ', end='')
            # construct workspace filename
            sname_sch_b = sname_sch + f'_bin{bin_n}'
            SO_lab = ''
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            # copy workspace to current dir
            # shutil.copyfile(wsfile, os.path.join('.', 'workspace.root'))
            # coarse scan (using syst)
            syst = 'syst_coarse'
            # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
            # No need to scan a wide range if we know it's narrow.
            # grid_dict = {'LL':-75, 'UL':75, 'steps': 301}
            # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            # name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst)
            name_str = f'_coarse_{WC}'
            outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
            outfile_ = f'higgsCombine_coarse_{WC}.{METHOD}.mH120.root'
            outfile_ = os.path.join(outdir, outfile_)
            # cmd_str = construct_combine_cmd_str(WC, 'workspace.root', grid_dict, asi_str,
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                                name_str, with_syst=True, method=METHOD)
            print('Coarse scan to determine appropriate WC range and number of steps:')
            print(cmd_str)
            proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
            grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
            # loop through stat/syst
            for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
                print(f'Running "{syst_label}"')
                # update to the appropriate workspace file (stat only or with syst)
                wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
                wsfile = os.path.join(wsdir, wsfile)
                name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
                cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                    name_str, with_syst=syst_bool, method=METHOD)
                print(cmd_str)
                proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
            print(f'Finished running combine. Expected file output: {outfile}')
    # go back to original directory
    print(f'Going back to original directory...')
    os.chdir(start_dir)

# all subchannels in a channel
def run_combine_subchannels(channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                     Precision, PrecisionCoarse, stdout, verbose=0):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    wsdir = os.path.join(datacard_dir, 'workspaces', 'subchannel')
    outdir = os.path.join(datacard_dir, 'output', 'subchannel')
    os.chdir(outdir)
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
        # construct workspace filename
        SO_lab = ''
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        # coarse scan (using syst)
        syst = 'syst_coarse'
        # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
        # No need to scan a wide range if we know it's narrow.
        # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
        grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst)
        name_str = f'_coarse_{WC}'
        outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
        outfile_ = f'higgsCombine_coarse_{WC}.{METHOD}.mH120.root'
        outfile_ = os.path.join(outdir, outfile_)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=True, method=METHOD)
        print('Coarse scan to determine appropriate WC range and number of steps:')
        print(cmd_str)
        proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
        grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
            print(f'Running "{syst_label}"')
            # update to the appropriate workspace file (stat only or with syst)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                name_str, with_syst=syst_bool, method=METHOD)
            print(cmd_str)
            proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
        print(f'Finished running combine. Expected file output: {outfile}')
    # go back to original directory
    print(f'Going back to original directory...')
    os.chdir(start_dir)

# channels
def run_combine_channels(datacard_dict, WC, ScanType, Asimov, asi_str,
                     Precision, PrecisionCoarse, stdout, verbose=0):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    wsdir = os.path.join(datacard_dir, 'workspaces', 'channel')
    outdir = os.path.join(datacard_dir, 'output', 'channel')
    os.chdir(outdir)
    channels = datacard_dict.keys()
    for i, ch in enumerate(channels):
        WCs = versions_dict[ch]['EFT_ops']
        if not WC in WCs:
            continue
        print(f'Channel: {ch}', end=': ')
        v = versions_dict[ch]['v']
        version = f'v{v}'
        sname_ch = datacard_dict[ch]['info']['short_name']
        sname_sch = '_combined'
        SO_lab = ''
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        # coarse scan (using syst)
        syst = 'syst_coarse'
        # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
        # No need to scan a wide range if we know it's narrow.
        # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
        grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst)
        name_str = f'_coarse_{WC}'
        outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
        outfile_ = f'higgsCombine_coarse_{WC}.{METHOD}.mH120.root'
        outfile_ = os.path.join(outdir, outfile_)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=True, method=METHOD)
        print('Coarse scan to determine appropriate WC range and number of steps:')
        print(cmd_str)
        proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
        grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
            print(f'Running "{syst_label}"')
            # update to the appropriate workspace file (stat only or with syst)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                name_str, with_syst=syst_bool, method=METHOD)
            print(cmd_str)
            proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
        print(f'Finished running combine. Expected file output: {outfile}')
    # go back to original directory
    print(f'Going back to original directory...')
    os.chdir(start_dir)

# full analysis
def run_combine_full_analysis(WC, ScanType, Asimov, asi_str,
                     Precision, PrecisionCoarse, stdout, verbose=0):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    wsdir = os.path.join(datacard_dir, 'workspaces', 'full_analysis')
    outdir = os.path.join(datacard_dir, 'output', 'full_analysis')
    os.chdir(outdir)
    print('Full Analysis', end=': ')
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS'
    SO_lab = ''
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    # coarse scan (using syst)
    syst = 'syst_coarse'
    # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
    # No need to scan a wide range if we know it's narrow.
    # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
    # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
    grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
    # name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst)
    name_str = f'_coarse_{WC}'
    outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
    outfile_ = f'higgsCombine_coarse_{WC}.{METHOD}.mH120.root'
    outfile_ = os.path.join(outdir, outfile_)
    cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                        name_str, with_syst=True, method=METHOD)
    print('Coarse scan to determine appropriate WC range and number of steps:')
    print(cmd_str)
    proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
    grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
    # loop through stat/syst
    for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
        print(f'Running "{syst_label}"')
        # update to the appropriate workspace file (stat only or with syst)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='workspace', proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                            name_str, with_syst=syst_bool, method=METHOD)
        print(cmd_str)
        proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
    print(f'Finished running combine. Expected file output: {outfile}')
    # go back to original directory
    print(f'Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help=f'Which channel? ["all" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW", ...]')
    parser.add_argument('-s', '--ScanType',
                        help=f'What type of EFT scan was included in this file? ["_1D" (default),]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-p', '--Precision', help='What is desired precision / step size? e.g. "0.001" (default)')
    parser.add_argument('-pc', '--PrecisionCoarse', help='What is desired precision / step size when POI range > 10? e.g. "0.01" (default)')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 0 (default) / 1. "combine" output only included if Verbose>0.')
    args = parser.parse_args()
    if args.Channel is None:
        args.Channel = 'all'
    # list of channels
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WC_ALL
    else:
        WCs_loop = [args.WC]
    if args.ScanType is None:
        args.ScanType = '_1D'
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = '-t -1'
    else:
        asi_str = ''
    if args.Precision is None:
        args.Precision = 0.001
    else:
        args.Precision = float(args.Precision)
    if args.PrecisionCoarse is None:
        args.PrecisionCoarse = 0.01
    else:
        args.PrecisionCoarse = float(args.PrecisionCoarse)
    if args.Verbose is None:
        args.Verbose = 0
    else:
        args.Verbose = int(args.Verbose)
    if args.Verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    #########################
    # outer loop (over WC)
    for WC in WCs_loop:
        print(f'WC: '+WC)
        #########################
        # bin calculations
        print('Running combine for each bin:')
        print('=================================================')
        for channel in channels:
            WCs = versions_dict[channel]['EFT_ops']
            if not WC in WCs:
                continue
            v = versions_dict[channel]['v']
            VERSION = f'v{v}'
            run_combine_bins(channel, VERSION, datacard_dict, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             Precision=args.Precision, PrecisionCoarse=args.PrecisionCoarse,
                             stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
        #########################
        # subchannel calculations
        print('Running combine for each subchannel:')
        print('=================================================')
        for channel in channels:
            WCs = versions_dict[channel]['EFT_ops']
            if not WC in WCs:
                continue
            v = versions_dict[channel]['v']
            VERSION = f'v{v}'
            run_combine_subchannels(channel, VERSION, datacard_dict, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             Precision=args.Precision, PrecisionCoarse=args.PrecisionCoarse,
                             stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
        # '''
        #########################
        # channel calculations
        print('Running combine for each channel:')
        print('=================================================')
        run_combine_channels(datacard_dict, WC=WC,
                         ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                         Precision=args.Precision, PrecisionCoarse=args.PrecisionCoarse,
                         stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
        #########################
        # full analysis calculation
        print('Running combine for full analysis:')
        print('=================================================')
        run_combine_full_analysis(WC=WC,
                         ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                         Precision=args.Precision, PrecisionCoarse=args.PrecisionCoarse,
                         stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
        #########################
        # '''
