'''
Specialized script for estimating sensitivity to the SM. Will run at channel and full analysis levels.

To make sure up to date datacards and ROOT yield files are used, please ensure
scripts/tools/SM_combine_cards.py
has been run.
'''
import os
from time import time
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
    dim6_ops,
)

# FIXME! method should be a cmdline arg, but need to make sure it works
METHOD = 'MultiDimFit'

# for finding appropriate scan range
rangescript = os.path.join(datacard_dir, 'scripts', 'tools', 'find_POI_range.py')

secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
--X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
--stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"""

extra_no_backout = " --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT"

# str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
# x_flag = '--X-allow-no-signal'
### SM RUN
#combine -M MultiDimFit SM.all_combined.DataCard_Yields.v18.txt --algo=grid --points 601 --alignEdges 1 -t -1 --freezeNuisanceGroups nosyst --rMin -2 --rMax 4 --expectSignal 1 --verbose -1 -n _Full_SM_Test

# utility functions
def construct_combine_cmd_str(datacard_file, grid_dict, asimov_str,
                              name_str, with_syst=True, method='MultiDimFit', expect_signal='1', with_extra=True, Backout=False):
    points = grid_dict['steps']
    LL = grid_dict['LL']
    UL = grid_dict['UL']
    cmd_str = 'combine -M %s %s --algo=grid --points %s ' % (method, datacard_file, points)
    cmd_str += '--alignEdges 1 %s ' % asimov_str
    if with_syst:
        freeze_group = 'nosyst'
    else:
        freeze_group = 'allsyst'
    cmd_str += '--freezeNuisanceGroups %s ' % freeze_group
    # range of r
    cmd_str += '--rMin %s --rMax %s ' % (LL, UL)
    # signal injection?
    if not expect_signal is None:
        cmd_str += '--expectSignal %s ' % expect_signal
    cmd_str += '--verbose -1 -n %s' % name_str
    if with_extra:
        cmd_str += secret_options
    if not Backout:
        # args to prevent backout from regions with negative yield
        cmd_str += extra_no_backout
    return cmd_str


# channels
def run_combine_channels(channels, datacard_dict, Asimov, asi_str,
                     Precision, stdout, expect_signal='1', LL=-2, UL=4, verbose=0, Backout=False):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if expect_signal is None:
        suff_purp = '_expect_signal_0'
    else:
        suff_purp = '_expect_signal_' + expect_signal
    outdir = os.path.join(datacard_dir, 'output', 'channel')
    os.chdir(outdir)
    for i, ch in enumerate(channels):
        print('Channel: %s' % ch)
        v = versions_dict[ch]['v']
        version = 'v' + str(v)
        sname_ch = datacard_dict[ch]['info']['short_name']
        sname_sch = '_combined'
        # set up grid dict
        grid_dict = {'LL': LL, 'UL': UL}
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/Precision) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * Precision
        # filename to print at the end
        outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC='sm',ScanType='',version=version,syst='syst', method=METHOD)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
            print('Running "%s"' % syst_label)
            dc_file = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC='REMOVE', ScanType='', purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
            dc_file = dc_file.replace('VVV.', 'SM.').replace('.REMOVE.', '.')
            dc_file = os.path.join(datacard_dir, 'combined_datacards', 'channel', dc_file)
            name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC='sm',ScanType='',version=version,syst=syst_label)
            cmd_str = construct_combine_cmd_str(dc_file, grid_dict, asi_str,
                                                name_str, with_syst=syst_bool,
                                                method=METHOD, expect_signal=expect_signal,
                                                Backout=Backout)
            print(cmd_str)
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        print('Finished running combine. Expected file output: %s' % outfile)
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)

# full analysis
def run_combine_full_analysis(Asimov, asi_str, Precision,
                              stdout, expect_signal='1', LL=-2, UL=4, verbose=0, Backout=False):
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if expect_signal is None:
        suff_purp = '_expect_signal_0'
    else:
        suff_purp = '_expect_signal_' + expect_signal
    outdir = os.path.join(datacard_dir, 'output', 'full_analysis')
    os.chdir(outdir)
    print('Full Analysis:')
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS'
    # set up grid dict
    grid_dict = {'LL': LL, 'UL': UL}
    grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/Precision) + 2
    grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * Precision
    # filename to print at the end
    outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC='sm',ScanType='',version=version,syst='syst', method=METHOD)
    # loop through stat/syst
    for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
        print('Running "%s"' % syst_label)
        dc_file = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC='REMOVE', ScanType='', purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
        dc_file = dc_file.replace('VVV.', 'SM.').replace('.REMOVE.', '.')
        dc_file = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis', dc_file)
        name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC='sm',ScanType='',version=version,syst=syst_label)
        cmd_str = construct_combine_cmd_str(dc_file, grid_dict, asi_str,
                                            name_str, with_syst=syst_bool,
                                            method=METHOD, expect_signal=expect_signal,
                                            Backout=Backout)
        print(cmd_str)
        proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    print('Finished running combine. Expected file output: %s' % outfile)
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run combine for? "all" (default). Any combination in any order of the following characters will work: "c" (channel), "f" (full analysis). e.g. "c" will run only the channel level.')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-e', '--ExpectSignal',
                        help='What expected signal should be used? e.g. "1" (default), "0", ..., "None". Note, if "None" the cmdline arg is removed when calling combine.')
    parser.add_argument('-p', '--Precision', help='What is desired precision / step size? e.g. "0.05" (default)')
    parser.add_argument('-l', '--LL', help='Lower limit in the grid scan? e.g. "-2" (default), "0", ...')
    parser.add_argument('-u', '--UL', help='Upper limit in the grid scan? e.g. "4" (default), "20", ...')
    parser.add_argument('-B', '--Backout',
                        help='Back out of regions where yield becomes negative? "n" (default), "y"')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 0 (default) / 1. "combine" output only included if Verbose>0.')
    args = parser.parse_args()
    if args.Channel is None:
        args.Channel = 'all'
    # list of channels
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if (args.theLevels is None) or (args.theLevels == 'all'):
        generate_ch = True
        generate_full = True
    else:
        if 'c' in args.theLevels:
            generate_ch = True
        else:
            generate_ch = False
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = '-t -1'
        args.Asimov=True
    else:
        asi_str = ''
        args.Asimov=False
    if args.ExpectSignal is None:
        #expect_signal = None
        expect_signal = '1'
    else:
        expect_signal = args.ExpectSignal.strip()
    if args.Precision is None:
        args.Precision = 0.001
    else:
        args.Precision = float(args.Precision)
    if args.LL is None:
        args.LL = -2.0
    else:
        args.LL = float(args.LL)
    if args.UL is None:
        args.UL = 4.0
    else:
        args.UL = float(args.UL)
    if args.Backout is None:
        Backout = 'n'
    else:
        Backout = args.Backout
    Backout_bool = Backout == 'y'
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
    # for WC in WCs_loop:
    for sig in ['sm']:
        print('Calculations for %s' % sig)
        #########################
        # channel calculations
        if generate_ch:
            print('Running combine for each channel:')
            print('=================================================')
            run_combine_channels(channels, datacard_dict, Asimov=args.Asimov,
                                 asi_str=asi_str, Precision=args.Precision,
                                 stdout=stdout, expect_signal=expect_signal,
                                 LL=args.LL, UL=args.UL, verbose=args.Verbose,
                                 Backout=Backout_bool)
            print('=================================================\n')
        #########################
        # full analysis calculation
        if generate_full:
            print('Running combine for full analysis:')
            print('=================================================')
            run_combine_full_analysis( Asimov=args.Asimov, asi_str=asi_str,
                             Precision=args.Precision, stdout=stdout,
                             expect_signal=expect_signal, LL=args.LL, UL=args.UL,
                             verbose=args.Verbose,
                             Backout=Backout_bool)
            print('=================================================\n')
        #########################
