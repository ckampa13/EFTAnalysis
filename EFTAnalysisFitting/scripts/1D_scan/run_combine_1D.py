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
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, WCs_clip_dim6, WCs_clip_dim8, WCs_NDIM
from MISC_CONFIGS import (
    datacard_dir,
    template_filename,
    template_outfilename,
    template_outfilename_stub,
    dim6_ops,
    prof_grid_dict,
    NPs_to_promote_dict,
    USE_NP_POI_DICT,
    clip_grid_dict,
)

# FIXME! method should be a cmdline arg, but need to make sure it works
METHOD = 'MultiDimFit'
# constant value to limit the WCs when profiling
###### GRID JOBS
# 07-02-25
# LIM_VAL = 10
# prof_freeze_WCs = []
# 07-03-25
# LIM_VAL = 20
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1']
# 07-07-25
# LIM_VAL = 10
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHl3']
# 07-08-25
# promoting PDF_, QCDScale_, jes_ to POIs for randomized initializations
# don't freeze anything
LIM_VAL = 20
prof_freeze_WCs = []
###### OLD BELOW
# LIM_VAL = 2 # keep to theoretically interesting values
# LIM_VAL = 10 # first grid run (07-02-25)
#LIM_VAL = 20
# LIM_VAL = 50
# LIM_VAL = 100
# LIM_VAL = 200 # DEFAULT
#LIM_VAL = 500

# always use the same list of WCs to freeze while profiling
# None (full treatment)
# prof_freeze_WCs = []
# turning some off
# unblinding (06-25-25)
# prof_freeze_WCs = []
# prof_freeze_WCs = ['cll1']
# prof_freeze_WCs = ['cll1', 'cHDD', 'cHbox']
# prof_freeze_WCs = ['cll1', 'cHDD', 'cHbox', 'cHW', 'cHq3', 'cHq1']
# prof_freeze_WCs = ['cll1', 'cHDD', 'cHbox', 'cHW', 'cHq3', 'cHq1', 'cHl3'] # GOOD, some WC match freeze and profile
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3'] # 5 weakest WCs
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3', 'cHWB', 'cHd', 'cHu', 'cW'] # freeze all but cHq1, cHq3, cHW -- these show the worst behavior
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3', 'cHWB', 'cHd', 'cHu', 'cW', 'cHW'] # freeze all but cHq1, cHq3
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3', 'cHWB', 'cHd', 'cHu', 'cW', 'cHW', 'cHq3'] # freeze all but cHq1
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3', 'cHWB', 'cHd', 'cHu', 'cW', 'cHW', 'cHq1'] # freeze all but cHq3
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHB', 'cHl3', 'cHWB', 'cHd', 'cHu', 'cW', 'cHq1', 'cHq3'] # freeze all but cHW
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHl3', 'cHq1', 'cHq3'] # FINAL (first pass) -- no impact on cW
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1'] # STOPPED HERE. FINAL (first pass) -- LIM_VAL=50
# prof_freeze_WCs = ['cHDD', 'cHbox', 'cll1', 'cHl3'] # FINAL (first pass) -- LIM_VAL=50
# TAU UNBLINDING
# prof_freeze_WCs = ['cHl3', 'cll1', 'cHDD', 'cHbox', 'cHB', 'cHWB', 'cHd'] # GOOD FOR cW
# prof_freeze_WCs = ['cHl3', 'cll1', 'cHDD', 'cHbox', 'cHB', 'cHWB', 'cHu']
# prof_freeze_WCs = ['cHl3', 'cll1', 'cHDD', 'cHbox', 'cHB', 'cHd']
# good with range -10,10 for 1L and combination with 2L_SS
#prof_freeze_WCs = ['cHl3', 'cll1', 'cHDD', 'cHbox', 'cHWB', 'cHB']
#prof_freeze_WCs = ['cHDD', 'cHbox', 'cHWB', 'cHB']
# 0L debug
# 50 limit
#prof_freeze_WCs = ['cHDD', 'cHbox', 'cHWB', 'cHB']
# prof_freeze_WCs = ['cHl3', 'cll1', 'cHDD', 'cHbox', 'cHWB', 'cHB'] # good -- results agree with 1D
#prof_freeze_WCs = ['cll1'] # good! some signs of bad behavior for larger cW (3FJ), but seems ok. mild degradation from 1D
# 2L_OS debugs -- SFZ fine, SFnoZ and OF weird
#prof_freeze_WCs = ['cHWB', 'cHDD', 'cHbox']
# prof_freeze_WCs = ['cll1']

# original
secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=1 \
--X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
--stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"""
####
# DEBUG (try to limit nuisance parameter ranges)
# also play with settings, e.g. MinimizerStrategy
# secret_options = """ --X-rtd MINIMIZER_respect_parameters_limits --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=1 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"""
# secret_options = """ --robustFit=0 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=1 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"""
# secret_options = """ --X-rtd=MINIMIZER_analytic"""
###
# extra options -- with outputs of best fit values for nuisances and profiled values
# secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --saveSpecifiedNuis all --trackParameters k_cW,k_cHq3,k_cHq1,k_cHu,k_cHd,k_cHW,k_cHWB,k_cHl3,k_cHB,k_cll1,k_cHbox,k_cHDD"""
# extra options -- with outputs of best fit values for nuisances and profiled values; include RooFit results
# secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --saveSpecifiedNuis all --trackParameters k_cW,k_cHq3,k_cHq1,k_cHu,k_cHd,k_cHW,k_cHWB,k_cHl3,k_cHB,k_cll1,k_cHbox,k_cHDD --saveFitResult
# """
# (modified by hand) extra options -- with outputs of best fit values for nuisances and profiled values
# prevent negative bin yields from forcing MIGRAD to back out of the region.
# secret_options = """ --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 \
# --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT \
# --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --saveSpecifiedNuis all"""# \
# --trackParameters k_cW,k_cHq3,k_cHq1,k_cHu,k_cHd,k_cHW,k_cHWB,k_cHl3,k_cHB,k_cll1,k_cHbox,k_cHDD"""

# extras
# don't back out of negative regions
extra_no_backout = " --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT"
extra_track_params = " --saveSpecifiedNuis all --trackParameters "
# random points to check for profile
random_prof_points_str = " --pointsRandProf=NUM_POINTS"

# for finding appropriate scan range
rangescript = os.path.join(datacard_dir, 'scripts', 'tools', 'find_POI_range.py')

# str_module = '-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
# x_flag = '--X-allow-no-signal'

# utility functions
def find_range(WC, output_file_name, Precision, PrecisionCoarse, Threshold=4.0):
    cmd_str = 'python3 %s -f %s -w %s -T %s ' % (rangescript, output_file_name, WC, Threshold)
    cmd_str += '-s %s -sc %s' % (Precision, PrecisionCoarse)
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    proc, err = proc.communicate()
    proc = proc.decode() # python3 returns byte string
    # print('find_range output: %s' % proc)
    # parse results
    grid_dict = {i.split(':')[0]:float(i.split(':')[1]) for i in proc.strip('\n').split(';')}
    grid_dict['steps'] = int(grid_dict['steps'])
    # CAUTION! debugging NDIM -- go at least to -1
    grid_dict['LL'] = min(grid_dict['LL'], -1.)
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
        ##prec = 0.1
        #print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/prec) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * prec
    # elif range_ > 4.5:
    elif range_ > 6.0:
        prec = 0.1
        #print('Using prec = 0.1')
        grid_dict['steps'] = int((grid_dict['UL']-grid_dict['LL'])/prec) + 2
        grid_dict['UL'] = grid_dict['LL'] + (grid_dict['steps'] - 1) * prec
    # elif range_ > 2.5:
    # elif range_ > 3.0:
    elif range_ > 4.5:
        #prec = 0.01
        prec = 0.05
        #print('Using prec = 0.01')
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
                              name_str, with_syst=True, method='MultiDimFit', WCs_freeze=None, WCs_limit=None, limit_val=20., with_extra=True, fastScan=False, Backout=False, TrackParams=False, WCs_all=dim6_WCs, random_prof_points='0', track_NPs=None):
    points = grid_dict['steps']
    LL = grid_dict['LL']
    UL = grid_dict['UL']
    cmd_str = 'combine -M %s %s --algo=grid --points %s ' % (method, workspace_file, points)
    cmd_str += '--alignEdges 1 %s --redefineSignalPOIs k_%s ' % (asimov_str, WC)
    if with_syst:
        freeze_group = 'nosyst'
    else:
        freeze_group = 'allsyst'
    nps_str = ''
    nps_val = ''
    if WCs_freeze is None:
        WCs_freeze = []
    if len(WCs_freeze) < 1:
        # print('WCs_freeze is None')
        if True:
        # if freeze_group == 'allsyst':
            cmd_str += '--freezeNuisanceGroups %s --freezeParameters r ' % freeze_group
        else:
            # TEST remove PDF
            cmd_str += '--freezeNuisanceGroups %s,badsyst --freezeParameters r ' % freeze_group
    else:
        WCs_ = ['k_'+w for w in WCs_freeze]
        WCs_str = ','.join(WCs_)
        # print(WCs_str)
        # if True:
        if freeze_group == 'allsyst':
            cmd_str += '--freezeNuisanceGroups %s --freezeParameters r,%s ' % (freeze_group, WCs_str)
        else:
            # TEST remove PDF
            # cmd_str += '--freezeNuisanceGroups %s,badsyst --freezeParameters r,%s ' % (freeze_group, WCs_str)
            # cHl3 1L debug: PDF, JES, JER freeze
            # nps_freeze = ['PDF_', 'jes_', 'jer_'] # fixes all problems
            # nps_freeze = ['PDF_', 'jes_'] # still fine with JER
            # nps_freeze = ['PDF_'] # BAD -- means JES is bad.
            # nps_freeze = ['jes_'] # everything is fine with JES frozen
            # dim8 debugs (e.g. FT0)
            # nps_freeze = ['PDF_', 'QCDScale', 'jes_'] # fixes all problems
            # nps_freeze = ['PDF_', 'QCDScale'] # fine
            # nps_freeze = ['PDF_'] # fine. issue must be PDF.
            nps_freeze = [] # nothing frozen
            if len(nps_freeze) > 0:
                np_pre = ','
                nps_str = np_pre + ','.join(nps_freeze)
                nps_val = np_pre + '=0,'.join(nps_freeze) + '=0'
            else:
                np_pre = ''
                nps_str = ''
                nps_val = ''
            cmd_str += '--freezeNuisanceGroups %s --freezeParameters r,%s%s ' % (freeze_group, WCs_str, nps_str)
    cmd_str += '--setParameters r=1%s --setParameterRanges k_%s=%s,%s' % (nps_val, WC, LL, UL)
    # add parameter ranges for NP?
    lim_NP = dict()
    # lim_NP = {'PDF_': ['-1', '1']}
    # lim_NP = {'PDF_': ['-0.8', '0.8']}
    # lim_NP = {'PDF_': ['-0.5', '0.5']}
    # lim_NP = {'PDF_': ['-0.2', '0.2']}
    # lim_NP = {'jes_': ['-1.0', '1.0']}
    if len(lim_NP) > 0:
        lim_NP_list = []
        for k, v in lim_NP.items():
            lim_NP_list.append('%s=%s,%s' % (k, v[0], v[1]))
        lim_NP_str = ':' + ':'.join(lim_NP_list)
        cmd_str += lim_NP_str
    if WCs_limit is None:
        # TEST LIMITING PDF
        # cmd_str += ':PDF_=-2,2'
        ###
        cmd_str += ' '
    else:
        WCs_ = ['k_'+w for w in WCs_limit]
        val = '%0.1f' % limit_val
        mval = '%0.1f' % -limit_val
        #WCs_str = ','.join(WCs_)
        # WCs_str = ''
        for WC_ in WCs_:
            cmd_str += ':%s=%s,%s' % (WC_, mval, val)
        # TEST LIMITING PDF
        # cmd_str += ':PDF_=-2,2'
        ###
        cmd_str += ' '
    # if fastScan:
    #     # appends to "syst" part of the output file
    #     name_str +='_fastScan'
    # if len(lim_NP) > 0:
    #     lim_NP_list = []
    #     for k, v in lim_NP.items():
    #         lim_NP_list.append('%s=%s,%s' % (k, v[0], v[1]))
    #     lim_NP_str = '--setPhysicsModelParameterRanges ' + ':'.join(lim_NP_list)
    #     cmd_str += lim_NP_str + ' '
    cmd_str += '--verbose -1 -n %s' % name_str
    if with_extra:
        cmd_str += secret_options
    if fastScan:
        # nuisance parameters are fixed to their best-fit values
        cmd_str += ' --fastScan'
    if not Backout:
        # args to prevent backout from regions with negative yield
        cmd_str += extra_no_backout
    if TrackParams:
        # add nuisance tracking and POIs
        cmd_str += extra_track_params
        cmd_str += ','.join(['k_'+w for w in WCs_all])
        # track NPs promoted to POI
        if not track_NPs is None:
            cmd_str += ',' + ','.join(track_NPs)
    # random prof points
    if int(random_prof_points) > 0:
        cmd_str += random_prof_points_str.replace('NUM_POINTS', random_prof_points)
    return cmd_str

# all bins in a subchannel / channel
def run_combine_bins(dim, channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                     Precision, PrecisionCoarse, stdout, verbose=0, vsuff='', WCs_list=WC_ALL, fastScan=False, LinearOnly=False, Backout=False, TrackParams=False, Unblind=False, JustPrint=False, UseProfileGridDict=False, PointsRandProf='0', PointsRandProfStat=True):
    version_full = version + vsuff
    if dim == 'dim6':
        WCs_track = dim6_WCs
    else:
        WCs_track = dim8_WCs
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if PointsRandProfStat:
        PRPS = PointsRandProf
    else:
        PRPS = '0'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'single_bin')
    outdir = os.path.join(dcdir, 'output', 'single_bin')
    os.chdir(outdir)
    # add any frozen WC
    if ScanType == '_1D':
        WCs_freeze = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        #WCs_freeze = None
        WCs_freeze = []
        for WC_ in prof_freeze_WCs:
            if WC != WC_:
                WCs_freeze.append(WC_)
        WCs_limit = []
        for WC_ in WCs_list:
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
            SO_lab = '' # with syst
            # SO_lab = '_StatOnly' # stat only
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace', proc=SO_lab, version=version_full, file_type='root')
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
            # override if doing linear only
            if LinearOnly:
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            # use profile grid dict?
            if UseProfileGridDict:
                if '_clip_mVVV' in vsuff:
                    grid_dict = clip_grid_dict[WC]
                else:
                    grid_dict = prof_grid_dict[WC]
            #name_str = '_coarse_%s_%s_%s' % (WC, channel, str(time()))
            name_str = '_coarse_%s_%s_%s_%s' % (WC, channel, version_full, str(time()))
            outfile = template_outfilename.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst, method=METHOD)
            outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
            outfile_ = os.path.join(outdir, outfile_)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                                name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                                # name_str, with_syst=False, method=METHOD, WCs_freeze=WCs_freeze,
                                                WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                                Backout=Backout, TrackParams=False, WCs_all=WCs_track,
                                                random_prof_points=PointsRandProf)
            if not JustPrint:
                print('Coarse scan to determine appropriate WC range and number of steps:')
            if not UseProfileGridDict:
                print(cmd_str)
                if JustPrint:
                    grid_dict_f = grid_dict
                    prec= Precision
                else:
                    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
                    grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
            else:
                grid_dict_f = grid_dict
                prec= Precision
            # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=6.0)
            # loop through stat/syst
            for syst_bool, syst_label, SO_lab, PRP in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly'], [PointsRandProf, PRPS]):
                if not JustPrint:
                    print('Running "%s"' % syst_label)
                # update to the appropriate workspace file (stat only or with syst)
                wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch_b, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace', proc=SO_lab, version=version_full, file_type='root')
                wsfile = os.path.join(wsdir, wsfile)
                name_str = template_outfilename_stub.substitute(asimov=asi, channel=sname_ch,subchannel=sname_sch_b,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst_label+FS_suff)
                cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                    name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                                    WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                                    Backout=Backout, TrackParams=TrackParams, WCs_all=WCs_track,
                                                    random_prof_points=PRP)
                print(cmd_str)
                if not JustPrint:
                    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
            if not JustPrint:
                print('Finished running combine. Expected file output: %s' % outfile)
            # remove coarse file, else they will build up (added time)
            if not JustPrint and not UseProfileGridDict:
                os.remove(outfile_)
    # go back to original directory
    if not JustPrint:
        print('Going back to original directory...')
    os.chdir(start_dir)

# all subchannels in a channel
def run_combine_subchannels(dim, channel, version, datacard_dict, WC, ScanType, Asimov, asi_str,
                     SignalInject, Precision, PrecisionCoarse, stdout, verbose=0, vsuff='', WCs_list=WC_ALL, fastScan=False, LinearOnly=False, Backout=False, TrackParams=False, Unblind=False, JustPrint=False, UseProfileGridDict=False, PointsRandProf='0', PointsRandProfStat=True):
    version_full = version + vsuff
    if dim == 'dim6':
        WCs_track = dim6_WCs
    else:
        WCs_track = dim8_WCs
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    if PointsRandProfStat:
        PRPS = PointsRandProf
    else:
        PRPS = '0'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'subchannel')
    outdir = os.path.join(dcdir, 'output', 'subchannel')
    os.chdir(outdir)
    # add any frozen WC
    if ScanType == '_1D':
        WCs_freeze = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        #WCs_freeze = None
        WCs_freeze = []
        WCs_limit = []
        for WC_ in prof_freeze_WCs:
            if WC != WC_:
                WCs_freeze.append(WC_)
        for WC_ in WCs_list:
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
        SO_lab = '' # with syst
        # SO_lab = '_StatOnly' # stat only
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
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
            #grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
                grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            else:
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        else:
            grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        # override if doing linear only
        if LinearOnly:
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # use profile grid dict?
        if UseProfileGridDict:
            if '_clip_mVVV' in vsuff:
                grid_dict = clip_grid_dict[WC]
            else:
                grid_dict = prof_grid_dict[WC]
        #name_str = '_coarse_%s_%s_%s' % (WC, channel, str(time()))
        name_str = '_coarse_%s_%s_%s_%s' % (WC, channel, version_full, str(time()))
        outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst, method=METHOD)
        outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
        outfile_ = os.path.join(outdir, outfile_)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                            # name_str, with_syst=False, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                            Backout=Backout, TrackParams=False, WCs_all=WCs_track,
                                            random_prof_points=PointsRandProf)
        if not JustPrint:
            print('Coarse scan to determine appropriate WC range and number of steps:')
        if not UseProfileGridDict:
            print(cmd_str)
            if JustPrint:
                grid_dict_f = grid_dict
                prec= Precision
            else:
                proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
                grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
        else:
            grid_dict_f = grid_dict
            prec= Precision
        # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=6.0)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab, PRP in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly'], [PointsRandProf, PRPS]):
            if not JustPrint:
                print('Running "%s"' % syst_label)
            # update to the appropriate workspace file (stat only or with syst)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst_label+FS_suff)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                                WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                                Backout=Backout, TrackParams=TrackParams, WCs_all=WCs_track,
                                                random_prof_points=PRP)
            print(cmd_str)
            if not JustPrint:
                proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        if not JustPrint:
            print('Finished running combine. Expected file output: %s' % outfile)
        # remove coarse file, else they will build up (added time)
        if not JustPrint and not UseProfileGridDict:
            os.remove(outfile_)
    # go back to original directory
    if not JustPrint:
        print('Going back to original directory...')
    os.chdir(start_dir)

# channels
def run_combine_channels(dim, channels, datacard_dict, WC, ScanType, Asimov, asi_str, SignalInject,
                     Precision, PrecisionCoarse, stdout, verbose=0, vsuff='', WCs_list=WC_ALL, fastScan=False, LinearOnly=False, Backout=False, TrackParams=False, Unblind=False, JustPrint=False, UseProfileGridDict=False, PointsRandProf='0', PointsRandProfStat=True, PromoteNPs=False):
    if dim == 'dim6':
        WCs_track = dim6_WCs
    else:
        WCs_track = dim8_WCs
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    if PointsRandProfStat:
        PRPS = PointsRandProf
    else:
        PRPS = '0'
    track_NPs = None
    if PromoteNPs:
        if WC in USE_NP_POI_DICT[dim]:
            ws_suff = '_NPsPromote' # FIXME! Add to arguments?
            track_NPs = NPs_to_promote_dict[dim]
        else:
            ws_suff = ''
    else:
        ws_suff = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'channel')
    outdir = os.path.join(dcdir, 'output', 'channel')
    os.chdir(outdir)
    # add any frozen WC
    if ScanType == '_1D':
        WCs_freeze = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        # TEST FOR YULUN'S WWW SAMPLE (no sensitivity to cHB, cHu, cHd)
        WCs_freeze = []
        # if not WC == 'cHB':
        #     WCs_freeze.append('cHB')
        # if not WC == 'cHu':
        #     WCs_freeze.append('cHu')
        # if not WC == 'cHd':
        #     WCs_freeze.append('cHd')
        # adding others with <1% total contribution (quad)
        # if not WC == 'cHDD':
        #     WCs_freeze.append('cHDD')
        # if not WC == 'cll1':
        #     WCs_freeze.append('cll1')
        # if not WC == 'cHWB':
        #     WCs_freeze.append('cHWB')
        # if not WC == 'cHbox':
        #     WCs_freeze.append('cHbox')
        # adding all the others...
        # if not WC == 'cHq3':
        #     WCs_freeze.append('cHq3')
        # if not WC == 'cHq1':
        #     WCs_freeze.append('cHq1')
        # if not WC == 'cHW':
        #     WCs_freeze.append('cHW')
        # if not WC == 'cHl3':
        #     WCs_freeze.append('cHl3')
        #WCs_limit = None
        for WC_ in prof_freeze_WCs:
            if WC != WC_:
                WCs_freeze.append(WC_)
        #'''
        # BETTER
        # WCs_freeze = None
        WCs_limit = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_limit.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_limit.append(WC_)
        #'''
    # channels = datacard_dict.keys()
    for i, ch in enumerate(channels):
        WCs = versions_dict[ch]['EFT_ops']
        if not WC in WCs:
            continue
        print('Channel: %s' % ch)
        # v = versions_dict[ch]['v']
        if vsuff == '_NDIM':
            v = versions_dict[ch]['v_NDIM']
        else:
            v = versions_dict[ch]['v']
        version = 'v' + str(v)
        version_full = version + vsuff
        sname_ch = datacard_dict[ch]['info']['short_name']
        sname_sch = '_combined'
        SO_lab = '' # with syst
        # SO_lab = '_StatOnly' # stat only
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp+ws_suff, proc=SO_lab, version=version_full, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        # coarse scan (using syst)
        syst = 'syst_coarse'
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
        if ScanType == '_1D':
            # grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            # nominal
            '''
            if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
                grid_dict = {'LL': -10, 'UL': 10, 'steps': 21}
            elif WC in ['cHWB', 'cHl3', 'cHB', 'cll1']:
                grid_dict = {'LL': -50, 'UL': 50, 'steps': 101}
            else:
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            '''
            # TAU UNBLIND
            if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
                grid_dict = {'LL': -10, 'UL': 10, 'steps': 21}
            elif WC in ['cHWB', 'cHl3', 'cll1']:
                grid_dict = {'LL': -50, 'UL': 50, 'steps': 101}
            elif WC in ['cHDD']:
                grid_dict = {'LL': -200, 'UL': 200, 'steps': 201}
            elif WC in ['FT4', 'FT7', 'FS0', 'FS1', 'FS2']:
                grid_dict = {'LL': -150, 'UL': 150, 'steps': 201}
            elif WC in ['FT9', 'FM2', 'FM3', 'FM4', 'FM5']:
                grid_dict = {'LL': -200, 'UL': 200, 'steps': 201}
            else:
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        else:
            if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
                grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            elif WC in ['cHl3']:
                grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
                # grid_dict = {'LL':-30, 'UL':30, 'steps': 61}
            else:
                grid_dict = {'LL':-30, 'UL':30, 'steps': 61}
            #grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        # override if doing linear only
        if LinearOnly:
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # use profile grid dict?
        if UseProfileGridDict:
            if '_clip_mVVV' in vsuff:
                grid_dict = clip_grid_dict[WC]
            else:
                grid_dict = prof_grid_dict[WC]
        #name_str = '_coarse_%s_%s_%s' % (WC, ch, str(time()))
        name_str = '_coarse_%s_%s_%s_%s' % (WC, ch, version_full, str(time()))
        outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst, method=METHOD)
        outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
        outfile_ = os.path.join(outdir, outfile_)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                            name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                            # name_str, with_syst=False, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                            Backout=Backout, TrackParams=False, WCs_all=WCs_track,
                                            # random_prof_points=PointsRandProf) # no pointsRandProf on init scan (??)
                                            random_prof_points='0', track_NPs=track_NPs) # no pointsRandProf on init scan (??)
        if not JustPrint:
            print('Coarse scan to determine appropriate WC range and number of steps:')
        if not UseProfileGridDict:
            print(cmd_str)
            if JustPrint:
                grid_dict_f = grid_dict
                prec= Precision
            else:
                proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
                grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
        else:
            grid_dict_f = grid_dict
            prec= Precision
        # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=6.0)
        # loop through stat/syst
        for syst_bool, syst_label, SO_lab, ws_suff_, track_NPs_, PRP in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly'], [ws_suff, ''], [track_NPs, None], [PointsRandProf, PRPS]):
            if not JustPrint:
                print('Running "%s"' % syst_label)
            # update to the appropriate workspace file (stat only or with syst)
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp+ws_suff_, proc=SO_lab, version=version_full, file_type='root')
            wsfile = os.path.join(wsdir, wsfile)
            name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version_full,syst=syst_label+FS_suff)
            cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                                name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                                WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                                Backout=Backout, TrackParams=TrackParams, WCs_all=WCs_track,
                                                random_prof_points=PRP, track_NPs=track_NPs_)
            print(cmd_str)
            # proc = subprocess.run(cmd_str, stdout=stdout, shell=True)
            if not JustPrint:
                proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        if not JustPrint:
            print('Finished running combine. Expected file output: %s' % outfile)
        # remove coarse file, else they will build up (added time)
        if not JustPrint and not UseProfileGridDict:
            os.remove(outfile_)
    # go back to original directory
    if not JustPrint:
        print('Going back to original directory...')
    os.chdir(start_dir)

# full analysis
def run_combine_full_analysis(dim, WC, ScanType, Asimov, asi_str, SignalInject,
                     Precision, PrecisionCoarse, stdout, verbose=0, vsuff='', WCs_list=WC_ALL, fastScan=False, LinearOnly=False, Backout=False, TrackParams=False, Unblind=False, JustPrint=False, UseProfileGridDict=False, PointsRandProf='0', PointsRandProfStat=True, PromoteNPs=False):
    if dim == 'dim6':
        WCs_track = dim6_WCs
    else:
        WCs_track = dim8_WCs
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        ScanTypeWS = '_All'
    else:
        ScanTypeWS = ScanType
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    start_dir = os.getcwd()
    if Asimov:
        asi = 'Asimov'
    else:
        asi = 'Data'
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    if PointsRandProfStat:
        PRPS = PointsRandProf
    else:
        PRPS = '0'
    track_NPs = None
    if PromoteNPs:
        if WC in USE_NP_POI_DICT[dim]:
            ws_suff = '_NPsPromote' # FIXME! Add to arguments?
            track_NPs = NPs_to_promote_dict[dim]
        else:
            ws_suff = ''
    else:
        ws_suff = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'full_analysis')
    outdir = os.path.join(dcdir, 'output', 'full_analysis')
    os.chdir(outdir)
    if not JustPrint:
        print('Full Analysis:')
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS'+vsuff
    SO_lab = '' # with syst
    # SO_lab = '_StatOnly' # stat only
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp+ws_suff, proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    # add any frozen WC
    if ScanType == '_1D':
        WCs_freeze = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_freeze.append(WC_)
        WCs_limit = None
    else:
        WCs_freeze = []
        # if not WC == 'cHB':
        #     WCs_freeze.append('cHB')
        # if not WC == 'cHu':
        #     WCs_freeze.append('cHu')
        # if not WC == 'cHd':
        #     WCs_freeze.append('cHd')
        # adding others with <1% total contribution (quad)
        # if not WC == 'cHDD':
        #     WCs_freeze.append('cHDD')
        # if not WC == 'cll1':
        #     WCs_freeze.append('cll1')
        # if not WC == 'cHWB':
        #     WCs_freeze.append('cHWB')
        # if not WC == 'cHbox':
        #     WCs_freeze.append('cHbox')
        # adding all the others...
        # if not WC == 'cHq3':
        #     WCs_freeze.append('cHq3')
        # if not WC == 'cHq1':
        #     WCs_freeze.append('cHq1')
        # if not WC == 'cHW':
        #     WCs_freeze.append('cHW')
        # if not WC == 'cHl3':
        #     WCs_freeze.append('cHl3')
        for WC_ in prof_freeze_WCs:
            if WC != WC_:
                WCs_freeze.append(WC_)
        #WCs_freeze = None
        WCs_limit = []
        for WC_ in WCs_list:
            if WC_ != WC:
                if (dim == 'dim6') and (WC_ in dim6_ops):
                    WCs_limit.append(WC_)
                elif (dim == 'dim8') and (not WC_ in dim6_ops):
                    WCs_limit.append(WC_)
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
        # grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # grid_dict = {'LL':-20, 'UL':20, 'steps': 41}
        # grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
        if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
            grid_dict = {'LL': -4, 'UL': 4, 'steps': 9}
        elif WC in ['cHl3']:
            grid_dict = {'LL':-23, 'UL':40, 'steps': 64}
        #elif WC in ['cHWB', 'cHl3', 'cHB', 'cll1']:
        #    grid_dict = {'LL': -50, 'UL': 50, 'steps': 101}
        #    #grid_dict = {'LL': -20, 'UL': 20, 'steps': 21}
        # else:
        #     grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        elif WC in ['cHbox', 'cHDD']:
            grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
        # TEMPORARY -- AN prep
        elif 'FS' in WC or WC in ['cll1']:
            grid_dict = {'LL':-40, 'UL':40, 'steps': 81}
        else:
            grid_dict = {'LL':-30, 'UL':30, 'steps': 61}
    else:
        if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']:
        # if WC in ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd']:
            grid_dict = {'LL':-5, 'UL':5, 'steps': 11}
            # grid_dict = {'LL':-3, 'UL':3, 'steps': 6}
        # elif WC in ['cHW']:
        #    grid_dict = {'LL':-3, 'UL':3, 'steps': 6}
        elif WC in ['cHl3']:
            # grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
            #grid_dict = {'LL':-30, 'UL':30, 'steps': 61}
            grid_dict = {'LL':-23, 'UL':40, 'steps': 64}
        else:
            grid_dict = {'LL':-30, 'UL':30, 'steps': 61}
    # override if doing linear only
    if LinearOnly:
        grid_dict = {'LL':-100, 'UL':100, 'steps': 201}
    # use profile grid dict?
    if UseProfileGridDict:
        if '_clip_mVVV' in vsuff:
            grid_dict = clip_grid_dict[WC]
        else:
            grid_dict = prof_grid_dict[WC]
    #name_str = '_coarse_%s_all_%s' % (WC, str(time()))
    name_str = '_coarse_%s_all_%s_%s' % (WC, version, str(time()))
    outfile = template_outfilename.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version,syst=syst, method=METHOD)
    outfile_ = 'higgsCombine%s.%s.mH120.root' % (name_str, METHOD)
    outfile_ = os.path.join(outdir, outfile_)
    cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict, asi_str,
                                        name_str, with_syst=True, method=METHOD, WCs_freeze=WCs_freeze,
                                        # name_str, with_syst=False, method=METHOD, WCs_freeze=WCs_freeze,
                                        WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                        Backout=Backout, TrackParams=False, WCs_all=WCs_track,
                                        # random_prof_points=PointsRandProf) # no pointsRandProf on init scan (??)
                                        random_prof_points='0', track_NPs=track_NPs) # no pointsRandProf on init scan (??)
    if not JustPrint:
        print('Coarse scan to determine appropriate WC range and number of steps:')
    if not UseProfileGridDict:
        print(cmd_str)
        # '''
        if JustPrint:
            grid_dict_f = grid_dict
            prec= Precision
        else:
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
            grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=4.0)
    else:
        grid_dict_f = grid_dict
        prec= Precision
    # grid_dict_f, prec = find_range(WC, outfile_, Precision, PrecisionCoarse, Threshold=6.0)
    # loop through stat/syst
    for syst_bool, syst_label, SO_lab, ws_suff_, track_NPs_, PRP in zip([True, False], ['syst', 'nosyst'], ['', '_StatOnly'], [ws_suff, ''], [track_NPs, None], [PointsRandProf, PRPS]):
        if not JustPrint:
            print('Running "%s"' % syst_label)
        # update to the appropriate workspace file (stat only or with syst)
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS+LinO_str, purpose='workspace'+suff_purp+ws_suff_, proc=SO_lab, version=version, file_type='root')
        wsfile = os.path.join(wsdir, wsfile)
        name_str = template_outfilename_stub.substitute(asimov=asi+suff_purp, channel=sname_ch,subchannel=sname_sch,WC=WC,ScanType=ScanType+LinO_str,version=version,syst=syst_label+FS_suff)
        cmd_str = construct_combine_cmd_str(WC, wsfile, grid_dict_f, asi_str,
                                            name_str, with_syst=syst_bool, method=METHOD, WCs_freeze=WCs_freeze,
                                            WCs_limit=WCs_limit, limit_val=LIM_VAL, fastScan=fastScan,
                                            Backout=Backout, TrackParams=TrackParams, WCs_all=WCs_track,
                                            random_prof_points=PRP, track_NPs=track_NPs_)
        print(cmd_str)
        if not JustPrint:
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    if not JustPrint:
        print('Finished running combine. Expected file output: %s' % outfile)
    # remove coarse file, else they will build up (added time)
    if not JustPrint and not UseProfileGridDict:
        os.remove(outfile_)
    # '''
    # go back to original directory
    if not JustPrint:
        print('Going back to original directory...')
    os.chdir(start_dir)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["all" (default), "dim6", "dim8", "NDIM", "cW", ...]')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run combine for? "all" (default). Any combination in any order of the following characters will work: "b" (bin), "s" (subchannel), "c" (channel), "f" (full analysis). e.g. "bsc" will run all but the full analysis.')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default), "_1D" (freeze WCs)]')
    parser.add_argument('-f', '--fastScan',
                        help='Do you want to run a "fast scan" where the nuisance parameters are fixed to best-fit values (instead of profiling)? "n" (default) / "y"')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be used. Note that Asimov must also be set to "n" for signal injection to work!  n(default)/y.')
    parser.add_argument('-p', '--Precision', help='What is desired precision / step size? e.g. "0.001" (default)')
    parser.add_argument('-pc', '--PrecisionCoarse', help='What is desired precision / step size when POI range > 10? e.g. "0.01" (default)')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    parser.add_argument('-L', '--LinearOnly',
                        help='Drop quadratic and mixed terms in the EFT model? "n" (default), "y"')
    parser.add_argument('-B', '--Backout',
                        help='Back out of regions where yield becomes negative? "n" (default), "y"')
    parser.add_argument('-T', '--TrackParams',
                        help='Save POI values from the scan (useful for profiling)? "n" (default), "y"')
    parser.add_argument('-J', '--JustPrint',
                        help='Construct the combine string but do no not run it? Useful e.g. for preparing grid jobs. "n" (default), "y"')
    parser.add_argument('-UP', '--UseProfGridDict',
                        help='Use the hard coded grid_dict for profiling WCs? "n" (default), "y"')
    parser.add_argument('-PRP', '--PointsRandProf',
                        help='How many random initializations of profiled params per point? "0" (default), "1", "2", ..., "49"')
    parser.add_argument('-PRPS', '--PointsRandProfStat',
                        help='Use pointsRandProf in StatOnly calculation? Usually want "n" for 1D scans and "y" for profiling scans. "y" (default) / n.')
    parser.add_argument('-PNP', '--PromoteNPs',
                        help='Use the workspaces with some NPs promoted to POIs? Useful e.g. to use --pointsRandProf on NPs, or limiting NP ranges. "n" (default) / "y"')
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
    elif args.WC == 'dim6':
        WCs_loop = dim6_WCs
    elif args.WC == 'dim8':
        WCs_loop = dim8_WCs
        # WCs_loop = ['FT4', 'FT5', 'FT6', 'FT7', 'FT8', 'FT9']
        # WCs_loop = ['FT4', 'FT7', 'FT9', 'FS0', 'FS1', 'FS2']
        # WCs_loop = ['FM0', 'FM1', 'FM2', 'FM3', 'FM4', 'FM5', 'FM7']
    elif args.WC == 'NDIM':
        WCs_loop = WCs_NDIM
    else:
        WCs_loop = [args.WC]
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
    if args.fastScan is None:
        fastScan = False
    else:
        fastScan = args.fastScan == 'y'
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
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    # cannot do bin level with signal injection
    if SignalInject:
        generate_bins = False
    # else:
    #     generate_bins = True
    if args.Precision is None:
        args.Precision = 0.001
    else:
        args.Precision = float(args.Precision)
    if args.PrecisionCoarse is None:
        args.PrecisionCoarse = 0.01
    else:
        args.PrecisionCoarse = float(args.PrecisionCoarse)
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    if args.LinearOnly is None:
        LinearOnly = 'n'
    else:
        LinearOnly = args.LinearOnly
    LinearOnly_bool = LinearOnly == 'y'
    if args.Backout is None:
        Backout = 'n'
    else:
        Backout = args.Backout
    Backout_bool = Backout == 'y'
    if args.TrackParams is None:
        TrackParams = 'n'
    else:
        TrackParams = args.TrackParams
    TrackParams_bool = TrackParams == 'y'
    if args.JustPrint is None:
        JustPrint = 'n'
    else:
        JustPrint = args.JustPrint
    JustPrint_bool = JustPrint == 'y'
    if args.UseProfGridDict is None:
        UseProfGridDict = 'n'
    else:
        UseProfGridDict = args.UseProfGridDict
    UseProfGridDict_bool = UseProfGridDict == 'y'
    if args.PointsRandProf is None:
        PointsRandProf = '0'
    else:
        PointsRandProf = args.PointsRandProf
    if args.PointsRandProfStat is None:
        PointsRandProfStat = 'y'
    else:
        PointsRandProfStat = args.PointsRandProfStat
    PointsRandProfStat_bool = PointsRandProfStat == 'y'
    if args.PromoteNPs is None:
        PromoteNPs = 'n'
    else:
        PromoteNPs = args.PromoteNPs
    PromoteNPs_bool = PromoteNPs == 'y'
    if args.Verbose is None:
        args.Verbose = 0
    else:
        args.Verbose = int(args.Verbose)
    if args.Verbose > 0:
        stdout = None
    else:
        stdout = subprocess.PIPE
    # update WCs_loop if we are clipping
    # FIXME! This is clunky and was only in place to avoid freezing WCs not present in the file
    # during development.
    # if "clip" in vsuff:
    #     WCs_ALL_ = []
    #     WCs_loop_new = []
    #     WCs_clip = WCs_clip_dim6 + WCs_clip_dim8
    #     for WC in WCs_loop:
    #         if WC in WCs_clip:
    #             WCs_loop_new.append(WC)
    #             WCs_ALL_.append(WC)
    #     WCs_loop = WCs_loop_new
    #     print('Clipping -- using an alternative set of WCs: %s' % str(WCs_loop))
    # else:
    #    WCs_ALL_ = WC_ALL
    WCs_ALL_ = WC_ALL

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
                                 #stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_loop)
                                 stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_ALL_,
                                 fastScan=fastScan, LinearOnly=LinearOnly_bool,
                                 Backout=Backout_bool, TrackParams=TrackParams_bool,
                                 Unblind=Unblind, JustPrint=JustPrint_bool,
                                 UseProfileGridDict=UseProfGridDict_bool,
                                 PointsRandProf=PointsRandProf, PointsRandProfStat=PointsRandProfStat_bool)#, PromoteNPs=PromoteNPs_bool)
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
                                 # stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_loop)
                                 stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_ALL_,
                                 fastScan=fastScan, LinearOnly=LinearOnly_bool,
                                 Backout=Backout_bool, TrackParams=TrackParams_bool,
                                 Unblind=Unblind, JustPrint=JustPrint_bool,
                                 UseProfileGridDict=UseProfGridDict_bool,
                                 PointsRandProf=PointsRandProf, PointsRandProfStat=PointsRandProfStat_bool)#, PromoteNPs=PromoteNPs_bool)
            print('=================================================\n')
        #########################
        # channel calculations
        if generate_ch:
            print('Running combine for each channel:')
            print('=================================================')
            run_combine_channels(dim, channels, datacard_dict, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             SignalInject=SignalInject, Precision=args.Precision,
                             PrecisionCoarse=args.PrecisionCoarse,
                             # stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_loop)
                             stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_ALL_,
                             fastScan=fastScan, LinearOnly=LinearOnly_bool,
                             Backout=Backout_bool, TrackParams=TrackParams_bool,
                             Unblind=Unblind, JustPrint=JustPrint_bool,
                             UseProfileGridDict=UseProfGridDict_bool,
                             PointsRandProf=PointsRandProf, PointsRandProfStat=PointsRandProfStat_bool, PromoteNPs=PromoteNPs_bool)
            print('=================================================\n')
        #########################
        # full analysis calculation
        if generate_full:
            print('Running combine for full analysis:')
            print('=================================================')
            run_combine_full_analysis(dim, WC=WC,
                             ScanType=args.ScanType, Asimov=args.Asimov, asi_str=asi_str,
                             SignalInject=SignalInject, Precision=args.Precision,
                             PrecisionCoarse=args.PrecisionCoarse,
                             # stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_loop)
                             stdout=stdout, verbose=args.Verbose, vsuff=vsuff, WCs_list=WCs_ALL_,
                             fastScan=fastScan, LinearOnly=LinearOnly_bool,
                             Backout=Backout_bool, TrackParams=TrackParams_bool,
                             Unblind=Unblind, JustPrint=JustPrint_bool,
                             UseProfileGridDict=UseProfGridDict_bool,
                             PointsRandProf=PointsRandProf, PointsRandProfStat=PointsRandProfStat_bool, PromoteNPs=PromoteNPs_bool)
            print('=================================================\n')
        #########################
