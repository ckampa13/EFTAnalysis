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

secret_options = """ --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT"""

def get_impact_commands(WC, workspace_file, asimov_str, name_str, json_name, plot_dir,
                        WCs_freeze=None, WCs_limit=None, limit_val=10., runBlind=False):
    # params_to_freeze = WCs
    cmd1 = 'combineTool.py -M Impacts -d %s -m 120 %s --redefineSignalPOIs k_%s --freezeNuisanceGroups nosyst ' % (workspace_file, asimov_str, WC)
    cmd2 = 'combineTool.py -M Impacts -d %s -m 120 %s --redefineSignalPOIs k_%s --freezeNuisanceGroups nosyst ' % (workspace_file, asimov_str, WC)
    cmd3 = 'combineTool.py -M Impacts -d %s -m 120 %s --redefineSignalPOIs k_%s --freezeNuisanceGroups nosyst ' % (workspace_file, asimov_str, WC)
    if WCs_freeze is None:
        cmd1 += '--freezeParameters r '
        cmd2 += '--freezeParameters r '
        cmd3 += '--freezeParameters r '
    else:
        WCs_ = ['k_'+w for w in WCs_freeze]
        WCs_str = ','.join(WCs_)
        cmd1 += '--freezeParameters r,%s ' % WCs_str
        cmd2 += '--freezeParameters r,%s ' % WCs_str
        cmd3 += '--freezeParameters r,%s ' % WCs_str
    # fix r param, set ranges
    cmd1 += '--setParameters r=1'
    cmd2 += '--setParameters r=1'
    cmd3 += '--setParameters r=1'
    # FIXME! Limit just the POI, or all WC?
    if WCs_limit is None:
        cmd1 += ' '
        cmd2 += ' '
        cmd3 += ' '
    else:
        WCs_ = ['k_'+w for w in WCs_limit]
        val = '%0.1f' % limit_val
        mval = '%0.1f' % -limit_val
        cmd1 += ' --setParameterRanges '
        cmd2 += ' --setParameterRanges '
        cmd3 += ' --setParameterRanges '
        for i, WC_ in enumerate(WCs_):
            if i > 0:
                cmd1 += ':'
                cmd2 += ':'
                cmd3 += ':'
            cmd1 += '%s=%s,%s' % (WC_, mval, val)
            cmd2 += '%s=%s,%s' % (WC_, mval, val)
            cmd3 += '%s=%s,%s' % (WC_, mval, val)
        cmd1 += ' '
        cmd2 += ' '
        cmd3 += ' '
    # robust fit
    cmd1 += '--robustFit 1 '
    cmd2 += '--robustFit 1 '
    cmd3 += '--robustFit 1 '
    # cmd specific1
    cmd1 += '--doInitialFit -n %s' % name_str
    # cmd2 += '--doFits -n %s' % name_str
    cmd2 += '--doFits -n %s --parallel 10' % name_str # launch multiple jobs
    cmd3 += ' -o %s.json -n %s' % (json_name, name_str)
    # plot impacts command
    if runBlind:
        # blinded
        cmd4 = 'plotImpacts.py -i %s.json -o %s --blind' % (json_name, json_name+'_blinded')
    else:
        # unblinded
        cmd4 = 'plotImpacts.py -i %s.json -o %s' % (json_name, json_name)
    # use secret options? (better convergence)
    # cmd1 += secret_options
    # cmd2 += secret_options
    # cmd3 += secret_options
    # mv from cwd to final plot directory
    cmd5 = 'mv %s.pdf %s' % (json_name+'_blinded', plot_dir)
    cmd6 = 'mv %s.pdf %s' % (json_name, plot_dir)
    # cmds = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7]
    cmds = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]
    return cmds

def run_impact_subchannels(dim, channel, version, datacard_dict, WC, limit_val,
                           ScanType, Asimov, asi_str, SignalInject, stdout, verbose=0, Unblind=False, runBlind=False):
    start_dir = os.getcwd()
    syst_label='syst'
    if runBlind:
        bl_label='_blindFlag'
    else:
        bl_label=''
    if ScanType == '_1D':
        scan_dir = 'freeze'
    else:
        scan_dir = 'profile'
    # plot_dir = os.path.join(datacard_dir, 'plots', 'subchannel', scan_dir)
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
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'subchannel')
    outdir = os.path.join(dcdir, 'output', 'subchannel')
    plot_dir = os.path.join(dcdir, 'plots', 'subchannel', scan_dir)
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
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    print('Channel: %s' % channel)
    for i, subch in enumerate(subchannels):
        print('Subchannel: %s' % subch)
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
        # construct workspace filename
        SO_lab = ''
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        name_str = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
        json_name = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
        # plot_name = os.path.join(plot_dir, 'Impacts'+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label))
        # print("json_name: %s, type: %s" % (json_name, str(type(json_name))))
        # print("plot_name: %s, type: %s" % (plot_name, str(type(plot_name))))
        cmds = get_impact_commands(WC, wsfile, asi_str, name_str, json_name, plot_dir,
                                   WCs_freeze=WCs_freeze, WCs_limit=[WC], limit_val=limit_val, runBlind=runBlind)
        for cmd in cmds:
            print(cmd)
            proc = subprocess.call(cmd, stdout=stdout, shell=True)
            print('\n\n')
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)

def run_impact_channel(dim, channel, version, datacard_dict, WC, limit_val, ScanType,
                       Asimov, asi_str, SignalInject, stdout, verbose=0, Unblind=False, runBlind=False):
    start_dir = os.getcwd()
    syst_label='syst'
    if runBlind:
        bl_label='_blindFlag'
    else:
        bl_label=''
    if ScanType == '_1D':
        scan_dir = 'freeze'
    else:
        scan_dir = 'profile'
    # plot_dir = os.path.join(datacard_dir, 'plots', 'channel', scan_dir)
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
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'channel')
    outdir = os.path.join(dcdir, 'output', 'channel')
    plot_dir = os.path.join(dcdir, 'plots', 'channel', scan_dir)
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
    sname_ch = datacard_dict[channel]['info']['short_name']
    sname_sch = '_combined'
    print('Channel: %s' % channel)
    SO_lab = ''
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    name_str = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
    json_name = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
    # plot_name = os.path.join(plot_dir, 'Impacts'+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label))
    cmds = get_impact_commands(WC, wsfile, asi_str, name_str, json_name, plot_dir,
                               WCs_freeze=WCs_freeze, WCs_limit=[WC], limit_val=limit_val, runBlind=runBlind)
    for cmd in cmds:
        print(cmd)
        proc = subprocess.call(cmd, stdout=stdout, shell=True)
        print('\n\n')
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)

def run_impact_full_analysis(dim, datacard_dict, WC, limit_val, ScanType, Asimov,
                             asi_str, SignalInject, stdout, verbose=0, Unblind=False, runBlind=False):
    start_dir = os.getcwd()
    syst_label='syst'
    if runBlind:
        bl_label='_blindFlag'
    else:
        bl_label=''
    if ScanType == '_1D':
        scan_dir = 'freeze'
    else:
        scan_dir = 'profile'
    # plot_dir = os.path.join(datacard_dir, 'plots', 'full_analysis', scan_dir)
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
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'full_analysis')
    outdir = os.path.join(dcdir, 'output', 'full_analysis')
    plot_dir = os.path.join(dcdir, 'plots', 'full_analysis', scan_dir)
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
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS'
    # print('Channel: %s' % channel)
    SO_lab = ''
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    name_str = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
    json_name = 'Impacts'+bl_label+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
    # plot_name = os.path.join(plot_dir, 'Impacts'+template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst_label))
    cmds = get_impact_commands(WC, wsfile, asi_str, name_str, json_name, plot_dir,
                               WCs_freeze=WCs_freeze, WCs_limit=[WC], limit_val=limit_val, runBlind=runBlind)
    for cmd in cmds: # all commands
    # for cmd in cmds[:1]: # TESTING -- first command only
        print(cmd)
        proc = subprocess.call(cmd, stdout=stdout, shell=True)
        print('\n\n')
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["0Lepton_2FJ" (default), "0Lepton_3FJ", "1Lepton", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["cW" (default), ...]')
    parser.add_argument('-l', '--LimitValue',
                        help='What range do you want to use for the selected WC? [10 (default), 20, ...]')
    parser.add_argument('-t', '--theLevel',
                        help='Which levels of analysis to run combine for? Only one level may be run per script call: "s" (subchannel), "c" (channel), "f" (full analysis, default).')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default), "_1D" (freeze WCs)]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-rB', '--runBlind', help='Run with "--blind" to hide the signal strengths? Do this for initial unblinding phase. "n"(default)/"y".')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be used. Note that Asimov must also be set to "n" for signal injection to work!  n(default)/y.')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 1 (default) / 0. "combine" output only included if Verbose>0.')
    # parse args
    args = parser.parse_args()
    if args.Channel is None:
        args.Channel = '0Lepton_3FJ'
    if args.WC is None:
        args.WC = 'cW'
    if args.LimitValue is None:
        args.LimitValue = 10
    else:
        args.LimitValue = float(args.LimitValue)
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
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = '-t -1'
        args.Asimov=True
    else:
        asi_str = ''
        args.Asimov=False
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    if args.runBlind is None:
        args.runBlind = 'n'
    if args.runBlind == 'y':
        runBlind = True
    else:
        runBlind = False
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.Verbose is None:
        args.Verbose = 1
    else:
        args.Verbose = int(args.Verbose)
    if args.Verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    WC = args.WC
    print('WC: %s' % WC)
    if WC in dim6_ops:
        dim = 'dim6'
    else:
        dim = 'dim8'
    print(dim)
    # run the appropriate function
    channel = args.Channel
    if generate_subch:
        print('Making impact plot for each subchannel:')
        print('=================================================')
        WCs = versions_dict[channel]['EFT_ops']
        if WC in WCs:
            v = versions_dict[channel]['v']
            VERSION = 'v'+str(v)
            run_impact_subchannels(dim, channel, VERSION, datacard_dict, WC=WC,
                                   limit_val=args.LimitValue, ScanType=args.ScanType,
                                   Asimov=args.Asimov, asi_str=asi_str,
                                   SignalInject=SignalInject,
                                   stdout=stdout, verbose=args.Verbose,
                                   Unblind=Unblind, runBlind=runBlind)
    print('=================================================\n')
    if generate_ch:
        print('Making impact plot for the selected channel:')
        print('=================================================')
        WCs = versions_dict[channel]['EFT_ops']
        if WC in WCs:
            v = versions_dict[channel]['v']
            VERSION = 'v'+str(v)
            run_impact_channel(dim, channel, VERSION, datacard_dict, WC=WC,
                               limit_val=args.LimitValue, ScanType=args.ScanType,
                               Asimov=args.Asimov, asi_str=asi_str,
                               SignalInject=SignalInject,
                               stdout=stdout, verbose=args.Verbose,
                               Unblind=Unblind, runBlind=runBlind)
    print('=================================================\n')
    if generate_full:
        print('Making impact plot for full analysis:')
        print('=================================================')
        WCs = WC_ALL
        if WC in WCs:
            run_impact_full_analysis(dim, datacard_dict, WC=WC,
                                     limit_val=args.LimitValue, ScanType=args.ScanType,
                                     Asimov=args.Asimov, asi_str=asi_str,
                                     SignalInject=SignalInject,
                                     stdout=stdout, verbose=args.Verbose,
                                     Unblind=Unblind, runBlind=runBlind)
    print('=================================================\n')
