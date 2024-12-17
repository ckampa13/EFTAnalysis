'''
Generic running of combine for extracting EFT limits on a pair of WCs. Nominally this is the
"MultiDimFit". Runs the calculation at a single level (bin-by-bin,
subchannel, channel, full analysis, or all of the above).

To make sure up to date datacards, ROOT yield files, and workspaces are used, please ensure
scripts/tools/combine_cards.py, scripts/tools/split_yields.py(or run_split_yields.sh),
and scripts/tools/make_workspaces.py have all been run for the WC of interest.

Freezing other WCs or profiling them are both allowed.
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
    # template_outfilename,
    # template_outfilename_stub,
    template_outfilename_2D,
    template_outfilename_2D_stub,
    dim6_ops,
)

# FIXME! method should be a cmdline arg, but need to make sure it works
METHOD = 'MultiDimFit'
# constant value to limit the WCs when profiling
LIM_VAL = 10
# LIM_VAL = 20
#LIM_VAL = 100

# always use the same list of WCs to freeze while profiling
# None (full treatment)
prof_freeze_WCs = []
# full analysis
# prof_freeze_WCs = ['cll1']

# secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND
# """

# secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --saveSpecifiedNuis all --trackParameters k_cW,k_cHq3,k_cHq1,k_cHu,k_cHd,k_cHW,k_cHWB,k_cHl3,k_cHB,k_cll1,k_cHbox,k_cHDD
# """
# (modified by hand) extra options -- with outputs of best fit values for nuisances and profiled values
# prevent negative bin yields from forcing MIGRAD to back out of the region.
secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
--X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT \
--stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --saveSpecifiedNuis all --trackParameters k_cW,k_cHq3,k_cHq1,k_cHu,k_cHd,k_cHW,k_cHWB,k_cHl3,k_cHB,k_cll1,k_cHbox,k_cHDD"""


# for finding appropriate scan range
# FIXME! This has not been developed yet.
'''
rangescript = os.path.join(datacard_dir, 'scripts', 'tools', 'find_POI_range_2param.py')

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
    if range_ > 20.5:
        # prec = 1.0
        # print('Using prec = 1.0')
        # grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/1.) + 2
        # grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 1.
        prec = 0.1
        print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/0.1) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 0.1
    elif range_ > 4.5:
        prec = 0.1
        print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/0.1) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 0.1
    elif range_ > 2.5:
        prec = 0.01
        print('Using prec = 0.01')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/0.01) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * 0.01
    # elif range_ > 10:
    #     prec = args.PrecisionCoarse
    #     print('Using PrecisionCoarse')
    else:
        prec = args.Precision
        print('Using Precision')
    return grid_dict, prec
'''

def construct_combine_cmd_str(WC1, WC2, workspace_file, grid_dict, asimov_str,
                              name_str, with_syst=True, method='MultiDimFit', WCs_freeze=None, WCs_limit=None, limit_val=20., with_extra=True):
    points1 = grid_dict['steps1']
    LL1 = grid_dict['LL1']
    UL1 = grid_dict['UL1']
    points2 = grid_dict['steps2']
    LL2 = grid_dict['LL2']
    UL2 = grid_dict['UL2']
    #points = int(points1 * points2)
    # FIXME! Don't want to hard code this -- need a better calculation
    # points = 10000
    #points = 100
    points = 400
    cmd_str = 'combine -M %s %s --algo=grid --points %s ' % (method, workspace_file, points)
    cmd_str += '--alignEdges 1 %s --redefineSignalPOIs k_%s,k_%s ' % (asimov_str, WC1, WC2)
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
    cmd_str += '--setParameters r=1 --setParameterRanges k_%s=%s,%s:k_%s=%s,%s' % (WC1, LL1, UL1, WC2, LL2, UL2)
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
    if with_extra:
        cmd_str += secret_options
    return cmd_str

'''
# all bins in a subchannel / channel
def run_combine_bins(dim, channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
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
    wsdir = os.path.join(datacard_dir, 'workspaces', 'single_bin')
    outdir = os.path.join(datacard_dir, 'output', 'single_bin')
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
        # loop through bins
        bins = datacard_dict[channel]['subchannels'][subch]['bins']
        for bin_n in bins:
            print('bin%s' % str(bin_n))
            # construct workspace filename
            sname_sch_b = sname_sch + ('_bin%d' % bin_n)
            SO_lab = ''
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanTypeWS, purpose='workspace', proc=SO_lab, version=version, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            # coarse scan (using syst)
            syst = 'syst_coarse'
            # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
            # No need to scan a wide range if we know it's narrow.
            if ScanType == '_1D':
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
                # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            else:
                grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            name_str = '_coarse_%s_%s_%s' % (WC, channel, str(time()))
            outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
            outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
            outfile_ = os.path.join(outdir, outfile_)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                                name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                                WCs_limit=WCs_limit, limit_val=LIM_VAL)
            print('Coarse scan to determine appropriate WC range and number of steps:')
            print(cmd_str)
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
            grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
            # loop through stat/syst
            for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
                print('Running "%s"' % syst_label)
                # update to the appropriate workspace file (stat only or with syst)
                wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanTypeWS, purpose='workspace', proc=SO_lab, version=version, file_type='root')
                wsfile = os.path.join(wsdir, wsfile)
                name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType,version=version,syst=syst_label)
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
'''

'''
# all subchannels in a channel
def run_combine_subchannels(dim, channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                     SignalInject, Precision, PrecisionCoarse, stdout, verbose=0):
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
        # coarse scan (using syst)
        syst = 'syst_coarse'
        # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
        # No need to scan a wide range if we know it's narrow.
        # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
        # FIXME! This might not work for all WCs with injected signal. Be careful
        # if SignalInject:
        #     grid_dict = {'LL':-10, 'UL':10, 'steps': 201}
        # else:
        #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        if ScanType == '_1D':
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        else:
            grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        name_str = '_coarse_%s_%s_%s' % (WC, channel, str(time()))
        outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType,version=version,syst=syst, method=METHOD)
        outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
        outfile_ = os.path.join(outdir, outfile_)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL)
        print('Coarse scan to determine appropriate WC range and number of steps:')
        print(cmd_str)
        proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
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
'''

# channels
def run_combine_channels(dim, channels, datacard_dict, WC1, WC2, ScanType, Asimov, asi_str, SignalInject,
                         grid_dict, stdout, verbose=0, vsuff=''):
    # if ScanType == '_2D':
    #     ScanTypeWS = '_All'
    # else:
    #     ScanTypeWS = ScanType
    ScanTypeWS = '_All'
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    wsdir = os.path.join(datacard_dir, 'workspaces', 'channel')
    outdir = os.path.join(datacard_dir, 'output', 'channel')
    os.chdir(outdir)
    # add any frozen WC
    if ScanType == '_2D':
        WCs_freeze = []
        for WC_ in WC_ALL:
            if (WC_ != WC1) and (WC_ != WC2):
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        # TEST FOR YULUN'S WWW SAMPLE (no sensitivity to cHB, cHu, cHd)
        WCs_freeze = []
        # if (not WC1 == 'cHB') and (not WC2 == 'cHB'):
        #     WCs_freeze.append('cHB')
        # if (not WC1 == 'cHu') and (not WC2 == 'cHu'):
        #     WCs_freeze.append('cHu')
        # if (not WC1 == 'cHd') and (not WC2 == 'cHd'):
        #     WCs_freeze.append('cHd')
        # adding others with <1% total contribution (quad)
        # if (not WC1 == 'cHDD') and (not WC2 == 'cHDD'):
        #     WCs_freeze.append('cHDD')
        # if (not WC1 == 'cll1') and (not WC2 == 'cll1'):
        #     WCs_freeze.append('cll1')
        # if (not WC1 == 'cHl3') and (not WC2 == 'cHl3'):
        #     WCs_freeze.append('cHl3')
        # if (not WC1 == 'cHWB') and (not WC2 == 'cHWB'):
        #     WCs_freeze.append('cHWB')
        # if (not WC1 == 'cHbox') and (not WC2 == 'cHbox'):
        #     WCs_freeze.append('cHbox')
        # WCs_limit = None
        #'''
        # BETTER
        #WCs_freeze = None
        for WC_ in prof_freeze_WCs:
            #if WC != WC_:
            if (WC1 != WC_) and (WC2 != WC_):
                WCs_freeze.append(WC_)
        WCs_limit = []
        for WC_ in WC_ALL:
            if (WC_ != WC1) and (WC_ != WC2):
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_limit.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_limit.append(WC_)
        #'''
    # channels = datacard_dict.keys()
    for i, ch in enumerate(channels):
        WCs = versions_dict[ch]['EFT_ops']
        if (not WC1 in WCs) or (not WC2 in WCs):
            continue
        print('Channel: %s' % ch)
        v = versions_dict[ch]['v']
        version = 'v' + str(v)
        version_full = version + vsuff
        sname_ch = datacard_dict[ch]['info']['short_name']
        sname_sch = '_combined'
        SO_lab = ''
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        # coarse scan (using syst)
        # syst = 'syst_coarse'
        # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
        # No need to scan a wide range if we know it's narrow.
        # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # FIXME! This might not work for all WCs with injected signal. Be careful
        # if SignalInject:
        #     grid_dict = {'LL':-10, 'UL':10, 'steps': 201}
        # else:
        #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # if ScanType == '_1D':
        #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        #     # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        # else:
        #     grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        # name_str = '_coarse_%s_%s_%s_%s' % (WC1, WC2, ch, str(time()))
        syst = 'syst'
        outfile = template_outfilename_2D.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC1=WC1+'_',WC2=WC2,ScanType=ScanType,version=version_full,syst=syst, method=METHOD)
        # outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
        # outfile_ = os.path.join(outdir, outfile_)
        # cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
        #                                     name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
        #                                     WCs_limit=WCs_limit, limit_val=LIM_VAL)
        # print('Coarse scan to determine appropriate WC range and number of steps:')
        # print(cmd_str)
        # proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
            print('Running "%s"' % syst_label)
            # update to the appropriate workspace file (stat only or with syst)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            name_str = template_outfilename_2D_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC1=WC1+'_',WC2=WC2,ScanType=ScanType,version=version_full,syst=syst_label)
            cmd_str = construct_combine_cmd_str(WC1, WC2, wsfile, grid_dict, asi_str,
                                                name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                                WCs_limit=WCs_limit, limit_val=LIM_VAL)
            print(cmd_str)
            # proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        print('Finished running combine. Expected file output: %s' % outfile)
        # remove coarse file, else they will build up (added time)
        # os.remove(outfile_)
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)

# full analysis
def run_combine_full_analysis(dim, WC1, WC2, ScanType, Asimov, asi_str, SignalInject,
                              grid_dict, stdout, verbose=0, vsuff=''):
    # if ScanType == '_1D':
    #     ScanTypeWS = '_All'
    # else:
    #     ScanTypeWS = ScanType
    ScanTypeWS = '_All'
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    wsdir = os.path.join(datacard_dir, 'workspaces', 'full_analysis')
    outdir = os.path.join(datacard_dir, 'output', 'full_analysis')
    os.chdir(outdir)
    print('Full Analysis:')
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS'
    version_full = version + vsuff
    SO_lab = ''
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    # add any frozen WC
    if ScanType == '_2D':
        WCs_freeze = []
        for WC_ in WC_ALL:
            if (WC_ != WC1) and (WC_ != WC2):
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        # WCs_freeze = None
        WCs_freeze = []
        for WC_ in prof_freeze_WCs:
            if (WC1 != WC_) and (WC2 != WC_):
                WCs_freeze.append(WC_)
        WCs_limit = []
        for WC_ in WC_ALL:
            #if WC_ != WC:
            if (WC_ != WC1) and (WC_ != WC2):
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_limit.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_limit.append(WC_)
    # coarse scan (using syst)
    #syst = 'syst_coarse'
    # FIXME! Make this configurable in each channel (maybe in CONFIG_VERSIONS.py)
    # No need to scan a wide range if we know it's narrow.
    # grid_dict = {'LL':-10, 'UL':10, 'steps': 41}
    # grid_dict = {'LL':-100, 'UL':100, 'steps': 401}
    # FIXME! This might not work for all WCs with injected signal. Be careful
    # if SignalInject:
    #     grid_dict = {'LL':-10, 'UL':10, 'steps': 201}
    # else:
    #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
    # if ScanType == '_1D':
    #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
    #     # grid_dict = {'LL':-20, 'UL':20, 'steps': 41}
    #     # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
    # else:
    #     grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
    #name_str = '_coarse_%s_all_%s' % (WC, str(time()))
    syst = 'syst_coarse'
    outfile = template_outfilename_2D.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC1=WC1+'_',WC2=WC2,ScanType=ScanType,version=version_full,syst=syst, method=METHOD)
    # outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
    # outfile_ = os.path.join(outdir, outfile_)
    # cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
    #                                     name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
    #                                     WCs_limit=WCs_limit, limit_val=LIM_VAL)
    # print('Coarse scan to determine appropriate WC range and number of steps:')
    # print(cmd_str)
    # proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
    # loop through stat/syst
    for syst_bool, syst_label, SO_lab in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly']):
        print('Running "%s"' % syst_label)
        # update to the appropriate workspace file (stat only or with syst)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        name_str = template_outfilename_2D_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC1=WC1+'_',WC2=WC2,ScanType=ScanType,version=version_full,syst=syst_label)
        cmd_str = construct_combine_cmd_str(WC1, WC2, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL)
        print(cmd_str)
        proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    print('Finished running combine. Expected file output: %s' % outfile)
    # remove coarse file, else they will build up (added time)
    # os.remove(outfile_)
    # go back to original directory
    print('Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w1', '--WC1',
                        help='Which Wilson Coefficient to study along x axis? ["cW", "cHq3", ...]')
    parser.add_argument('-l1', '--LL1',
                        help='Lower limit of scan for WC1. -0.5 = default.')
    parser.add_argument('-u1', '--UL1',
                        help='Upper limit of scan for WC1. +0.5 = default.')
    parser.add_argument('-w2', '--WC2',
                        help='Which Wilson Coefficient to study along y axis? Note this cannot match args.WC1. ["cHq3", "cHq1", ...]')
    parser.add_argument('-l2', '--LL2',
                        help='Lower limit of scan for WC2. -1 = default.')
    parser.add_argument('-u2', '--UL2',
                        help='Upper limit of scan for WC2. +1 = default.')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run combine for? "all" (default) runs for channel and full analysis level. Any combination in any order of the following characters will work: "c" (channel), "f" (full analysis).')
                        # help='Which levels of analysis to run combine for? "all" (default). Any combination in any order of the following characters will work: "b" (bin), "s" (subchannel), "c" (channel), "f" (full analysis). e.g. "bsc" will run all but the full analysis.')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All2D" (default), "_2D" (freeze WCs)]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be used. Note that Asimov must also be set to "n" for signal injection to work!  n(default)/y.')
    parser.add_argument('-p1', '--Precision1', help='What is desired precision / step size for WC1? e.g. "0.01" (default)')
    parser.add_argument('-p2', '--Precision2', help='What is desired precision / step size for WC2? e.g. "0.01" (default)')
    # parser.add_argument('-pc', '--PrecisionCoarse', help='What is desired precision / step size when POI range > 10? e.g. "0.01" (default)')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    parser.add_argument('-V', '--Verbose', help='Include "combine" output? 0 (default) / 1. "combine" output only included if Verbose>0.')
    args = parser.parse_args()
    if args.Channel is None:
        args.Channel = 'all'
    # list of channels
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.WC1 is None:
        args.WC1 = 'cW'
    if args.LL1 is None:
        args.LL1 = -0.5
    else:
        args.LL1 = float(args.LL1)
    if args.UL1 is None:
        args.UL1 = 0.5
    else:
        args.UL1 = float(args.UL1)
    if args.WC2 is None:
        args.WC2 = 'cHq3'
    if args.LL2 is None:
        args.LL2 = -1.0
    else:
        args.LL2 = float(args.LL2)
    if args.UL2 is None:
        args.UL2 = 1.0
    else:
        args.UL2 = float(args.UL2)
    # if args.WC == 'all':
    #     WCs_loop = WC_ALL
    # else:
    #     WCs_loop = [args.WC]
    if (args.theLevels is None) or (args.theLevels == 'all'):
    # if (args.theLevels is None) or (args.theLevels == 'all'):
        # generate_bins = True
        # generate_subch = True
        generate_ch = True
        generate_full = True
    else:
        # if 'b' in args.theLevels:
        #     generate_bins = True
        # else:
        #     generate_bins = False
        # if 's' in args.theLevels:
        #     generate_subch = True
        # else:
        #     generate_subch = False
        if 'c' in args.theLevels:
            generate_ch = True
        else:
            generate_ch = False
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.ScanType is None:
        args.ScanType = '_All2D'
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
    # cannot do bin level with signal injection
    if SignalInject:
        generate_bins = False
    # else:
    #     generate_bins = True
    if args.Precision1 is None:
        # args.Precision1 = 0.001
        args.Precision1 = 0.01
    else:
        args.Precision1 = float(args.Precision1)
    if args.Precision2 is None:
        # args.Precision2 = 0.001
        args.Precision2 = 0.01
    else:
        args.Precision2 = float(args.Precision2)
    # if args.PrecisionCoarse is None:
    #     args.PrecisionCoarse = 0.01
    # else:
    #     args.PrecisionCoarse = float(args.PrecisionCoarse)
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
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
    print('WC1: %s, WC2: %s' % (args.WC1, args.WC2))
    if args.WC1 in dim6_ops:
        dim1 = 'dim6'
    else:
        dim1 = 'dim8'
    if args.WC2 in dim6_ops:
        dim2 = 'dim6'
    else:
        dim2 = 'dim8'
    if dim1 != dim2:
          raise ValueError("WC1 and WC2 are not of the same dim!!! dim WC1 (%s) = %s, dim WC2 (%s) = (%s)" % (args.WC1, dim1, args.WC2, dim2))
    print('dim1 = %s, dim2 = %s' % (dim1, dim2))
    dim = dim1
    # make the grid dict
    grid_dict = {}
    steps1 = int((args.UL1 - args.LL1) / args.Precision1)
    steps2 = int((args.UL2 - args.LL2) / args.Precision2)
    grid_dict['steps1'] = steps1
    grid_dict['steps2'] = steps2
    grid_dict['LL1'] = args.LL1
    grid_dict['UL1'] = args.UL1
    grid_dict['LL2'] = args.LL2
    grid_dict['UL2'] = args.UL2
    '''
    #########################
    # bin calculations
    if generate_bins:
        print('Running combine for each bin:')
        print('=================================================')
        for channel in channels:
            WCs = versions_dict[channel]['EFT_ops']
            if not WC in WCs:
                continue
            v = versions_dict[channel]['v']
            VERSION = 'v'+str(v)
            run_combine_bins(dim, channel, VERSION, datacard_dict, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             Precision=args.Precision, PrecisionCoarse=args.PrecisionCoarse,
                             stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
    #########################
    # subchannel calculations
    if generate_subch:
        print('Running combine for each subchannel:')
        print('=================================================')
        for channel in channels:
            WCs = versions_dict[channel]['EFT_ops']
            if not WC in WCs:
                continue
            v = versions_dict[channel]['v']
            VERSION = 'v'+str(v)
            run_combine_subchannels(dim, channel, VERSION, datacard_dict, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             SignalInject=SignalInject, Precision=args.Precision,
                             PrecisionCoarse=args.PrecisionCoarse,
                             stdout=stdout, verbose=args.Verbose)
        print('=================================================\n')
    '''
    #########################
    # channel calculations
    if generate_ch:
        print('Running combine for each channel:')
        print('=================================================')
        run_combine_channels(dim, channels, datacard_dict, WC1=args.WC1, WC2=args.WC2,
                         ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                         SignalInject=SignalInject, grid_dict=grid_dict,
                         stdout=stdout, verbose=args.Verbose, vsuff=vsuff)
        print('=================================================\n')
    #########################
    # full analysis calculation
    if generate_full:
        print('Running combine for full analysis:')
        print('=================================================')
        run_combine_full_analysis(dim, WC1=args.WC1, WC2=args.WC2,
                         ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                         SignalInject=SignalInject, grid_dict=grid_dict,
                         stdout=stdout, verbose=args.Verbose, vsuff=vsuff)
        print('=================================================\n')
    #########################
