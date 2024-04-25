'''
Tool to create impact plots for a particular level of the analysis
(subchannel, channel, full analysis), for a particular WC. If running at
subchannel level, all subchannels in the given channel will be run.

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
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import (
    datacard_dir,
    template_filename,
    template_outfilename,
    template_outfilename_stub,
    dim6_ops,
)

def get_impact_commands(wsfile, WCs_freeze=None):
    params_to_freeze = WCs
    cmd1 = 'combineTool.py -M Impacts -d %s -m 120 %s --redefineSignalPOIs k_%s --freezeNuisanceGroups nosyst ' % (wsfile, asimov_str, WC)
    cmd2 = 'combineTool.py -M Impacts -d %s -m 120 %s --redefineSignalPOIs k_%s --freezeNuisanceGroups nosyst ' % (wsfile, asimov_str, WC)
    if WCs_freeze is None:
        cmd1 += '--freezeParameters r '
    else:
        WCs_ = ['k_'+w for w in WCs_freeze]
        WCs_str = ','.join(WCs_)
        cmd_str += '--freezeParameters r,%s ' % WCs_str

# cmd1
    cmd1 += '--setParameters r=1 --setParameterRanges k_cW=-10,10 --doInitialFit --robustFit 1 -n 2L_OS'

# cmd 2
    --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-10,10 --robustFit 1 --doFits -n 2L_OS
    pass

def run_impact_subchannels(dim, channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                           SignalInject, Precision, PrecisionCoarse, stdout, verbose=0):
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    wsdir = os.path.join(datacard_dir, 'workspaces', 'subchannel')
    outdir = os.path.join(datacard_dir, 'output', 'subchannel')
    os.chdir(outdir)
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
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["0Lepton_2FJ" (default), "0Lepton_3FJ", "1Lepton", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["cW" (default), ...]')
    parser.add_argument('-t', '--theLevel',
                        help='Which levels of analysis to run combine for? Only one level may be run per script call: "s" (subchannel), "c" (channel), "f" (full analysis, default).')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default), "_1D" (freeze WCs)]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be used. Note that Asimov must also be set to "n" for signal injection to work!  n(default)/y.')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 0 (default) / 1. "combine" output only included if Verbose>0.')
    # parse args
    args = parser.parse_args()
    if args.Channel is None:
        args.Channel = '0Lepton_3FJ'
    if args.WC is None:
        args.WC = 'cW'
    generate_subch = False
    generate_ch = False
    generate_full = False
    if (args.theLevel is None):
        generate_full = True
    else:
        if args.theLevel == 's':
            generate_subch = True
        elif args.theLevel == 'c':
            generate_ch = True
        elif args.theLevel == 'f':
            generate_full = True
        else:
            raise ValueError('Unrecognrized analysis level "%s". Please rerun with one of the following: ["s", "c", "f"]')
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.Verbose is None:
        args.Verbose = 0
    else:
        args.Verbose = int(args.Verbose)
    if args.Verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    print('WC: %s' % WC)
    if WC in dim6_ops:
        dim = 'dim6'
    else:
        dim = 'dim8'
    print(dim)
    # run the appropriate function
    if generate_subch:
        print('Making impact plot for each subchannel:')
        print('=================================================')
        WCs = versions_dict[channel]['EFT_ops']
        if not WC in WCs:
            continue
        v = versions_dict[channel]['v']
        VERSION = 'v'+str(v)
        run_impact_subchannels(dim, channel, VERSION, datacard_dict, WC=WC,
                         ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                         SignalInject=SignalInject, Precision=args.Precision,
                         PrecisionCoarse=args.PrecisionCoarse,
                         stdout=stdout, verbose=args.Verbose)
    print('=================================================\n')


