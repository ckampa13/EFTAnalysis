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
from time import time
import subprocess
import shutil
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs
from MISC_CONFIGS import (
    datacard_dir,
    template_filename,
    template_outfilename,
    template_outfilename_stub,
    dim6_ops,
)

# FIXME! method should be a cmdline arg, but need to make sure it works
METHOD = 'MultiDimFit'
# constant value to limit the WCs when profiling
# LIM_VAL = 20
LIM_VAL = 100

# for finding appropriate scan range
rangescript = os.path.join(datacard_dir, 'scripts', 'tools', 'find_POI_range.py')

# str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
# x_flag = '--X-allow-no-signal'

# utility functions
def find_range(WC, output_file_name, Precision, PrecisionCoarse, Threshold=4.0):
    cmd_str = 'python %s -f %s -w %s -T %s ' % (rangescript, output_file_name, WC, Threshold)
    cmd_str += '-s %s -sc %s' % (Precision, PrecisionCoarse)
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    proc, err = proc.communicate()
    # print('find_range output: %s' % proc)
    # parse results
    grid_dict = {i.split(':')[0]:float(i.split(':')[1]) for i in proc.strip('\n').split(';')}
    grid_dict['steps'] = int(grid_dict['steps'])
    print('LL: %s; UL: %s; steps: %s' % (grid_dict['LL'], grid_dict['UL'], grid_dict['steps']))
    range_ = grid_dict["UL"] - grid_dict["LL"]
    # FIXME! I don't think "prec" is used anywhere...
    # also can switch from hard coding the very coarse precision if desired if range_ > 50: prec = 1.0
    prec = Precision
    if range_ > 20.5:
        prec = 1.0
        # print('Using prec = 1.0')
        # grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/1.) + 2
        # grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 1.
        # prec = 0.1
        # print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/prec) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * prec
    elif range_ > 4.5:
        prec = 0.1
        # print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/prec) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * prec
    elif range_ > 2.5:
        prec = 0.01
        # print('Using prec = 0.01')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/prec) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * prec
    # elif range_ > 10:
    #     prec = args.PrecisionCoarse
    #     print('Using PrecisionCoarse')
    else:
        prec = args.Precision
        print('Using Precision')
    return grid_dict, prec

def construct_combine_cmd_str(WC, workspace_file, grid_dict, asimov_str,
                              name_str, with_syst=True, method='MultiDimFit', WCs_freeze=None, WCs_limit=None, limit_val=20.):
    points = grid_dict['steps']
    LL = grid_dict['LL']
    UL = grid_dict['UL']
    cmd_str = 'combine -M %s %s --algo=grid --points %s ' % (method, workspace_file, points)
    cmd_str += '--alignEdges 1 %s --redefineSignalPOIs k_%s ' % (asimov_str, WC)
    if with_syst:
        freeze_group = 'nosyst'
    else:
        freeze_group = 'allsyst'
    if WCs_freeze is None:
        cmd_str += '--freezeNuisanceGroups %s --freezeParameters r ' % freeze_group
    else:
        WCs_ = ['k_'+w for w in WCs_freeze]
        WCs_str = ','.join(WCs_)
        cmd_str += '--freezeNuisanceGroups %s --freezeParameters r,%s ' % (freeze_group, WCs_str)
    cmd_str += '--setParameters r=1 --setParameterRanges k_%s=%s,%s' % (WC, LL, UL)
    if WCs_limit is None:
        cmd_str += ' '
    else:
        WCs_ = ['k_'+w for w in WCs_limit]
        val = '%0.1f' % limit_val
        mval = '%0.1f' % -limit_val
        #WCs_str = ','.join(WCs_)
        # WCs_str = ''
        for WC_ in WCs_:
            cmd_str += ':%s=%s,%s' % (WC_, mval, val)
        cmd_str += ' '
    cmd_str += '--verbose -1 -n %s' % name_str
    return cmd_str

# full analysis
def run_combine_full_analysis_leave_one_out(channel_leave_out, dim, WC, ScanType, Asimov, asi_str, SignalInject,
                     Precision, PrecisionCoarse, stdout, verbose=0):
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    wsdir = os.path.join(datacard_dir, 'workspaces', 'leave_one_out')
    outdir = os.path.join(datacard_dir, 'output', 'leave_one_out')
    os.chdir(outdir)
    print('Full Analysis:')
    sname_ch = 'all'
    sname_sch = '_combined_LOO_'+channel_leave_out
    version = 'vCONFIG_VERSIONS'
    SO_lab = ''
    # SO_lab = '_StatOnly' # stat only
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    # add any frozen WC
    if ScanType == '_1D':
        WCs_freeze = []
        for WC_ in WC_ALL:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        WCs_freeze = None
        WCs_limit = []
        for WC_ in WC_ALL:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_limit.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_limit.append(WC_)
    # coarse scan (using syst)
    syst = 'syst_coarse'
    if ScanType == '_1D':
        if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
            grid_dict = {'LL': -4, 'UL': 4, 'steps': 9}
        elif WC in ['cHWB', 'cHl3', 'cHB', 'cll1']:
            grid_dict = {'LL': -50, 'UL': 50, 'steps': 101}
        else:
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
    else:
        grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
    name_str = '_coarse_%s_all_LOO_%s_%s' % (WC, channel_leave_out, str(time()))
    outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
    outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
    outfile_ = os.path.join(outdir, outfile_)
    cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                        name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                        # name_str, with_syst=False, method=METHOD, WCs_freeze=WCs_freeze,
                                        WCs_limit=WCs_limit, limit_val=LIM_VAL)
    print('Coarse scan to determine appropriate WC range and number of steps:')
    print(cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
    # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=6.0)
    # loop through stat/syst
    for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
        print('Running "%s"' % syst_label)
        # update to the appropriate workspace file (stat only or with syst)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                            name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL)
        print(cmd_str)
        proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    print('Finished running combine. Expected file output: %s' % outfile)
    # remove coarse file, else they will build up (added time)
    os.remove(outfile_)
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel to leave out? ["all" (looping, not recommended), "all_tau", "0Lepton_2FJ" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["all" (default), "dim6", "dim8", "cW", ...]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default), "_1D" (freeze WCs)]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be used. Note that Asimov must also be set to "n" for signal injection to work!  n(default)/y.')
    parser.add_argument('-p', '--Precision', help='What is desired precision / step size? e.g. "0.005" (default)')
    parser.add_argument('-pc', '--PrecisionCoarse', help='What is desired precision / step size when POI range > 10? e.g. "0.5" (default)')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 0 (default) / 1. "combine" output only included if Verbose>0.')
    args = parser.parse_args()
    if args.Channel is None:
        # args.Channel = 'all'
        args.Channel = '0Lepton_2FJ'
    # list of channels
    if args.Channel == 'all':
        channels = datacard_dict.keys()+['all_tau']
    else:
        channels = [args.Channel]
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WC_ALL
    elif args.WC == 'dim6':
        WCs_loop = dim6_WCs
    elif args.WC == 'dim8':
        WCs_loop = dim8_WCs
    else:
        WCs_loop = [args.WC]
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = '-t -1'
        args.Asimov=True
    else:
        asi_str = ''
        args.Asimov=False
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.Precision is None:
        args.Precision = 0.005
    else:
        args.Precision = float(args.Precision)
    if args.PrecisionCoarse is None:
        args.PrecisionCoarse = 0.5
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
        print('WC: %s' % WC)
        if WC in dim6_ops:
            dim = 'dim6'
        else:
            dim = 'dim8'
        print(dim)
        #########################
        # full analysis calculation
        print('Running combine for full analysis (leave one out):')
        print('=================================================')
        for channel in channels:
            print('Leave out: %s' % channel)
            run_combine_full_analysis_leave_one_out(channel, dim, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             SignalInject=SignalInject, Precision=args.Precision,
                             PrecisionCoarse=args.PrecisionCoarse,
                             stdout=stdout, verbose=args.Verbose)
            print('=================================================\n')
        #########################
