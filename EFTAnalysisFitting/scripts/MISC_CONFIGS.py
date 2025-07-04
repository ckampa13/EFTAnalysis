import os
from string import Template


fpath = os.path.dirname(os.path.realpath(__file__))
# datacard_dir = os.path.abspath(os.path.join(fpath,'..', '..'))
datacard_dir = os.path.abspath(os.path.join(fpath,'..'))

# template_filename = Template("VVV.$channel$subchannel.$WC$ScanType.DataCard_Yields$proc.$version.$file_type")
template_filename_yields = Template("VVV.$channel$subchannel.$purpose$proc.$version.$file_type")
template_filename = Template("VVV.$channel$subchannel.$WC$ScanType.$purpose$proc.$version.$file_type")
template_outfilename = Template("higgsCombine_$asimov.$channel$subchannel.$WC$ScanType.$version.$syst.$method.mH120.root")
template_outfilename_stub = Template("_$asimov.$channel$subchannel.$WC$ScanType.$version.$syst")
# 2D scan
template_outfilename_2D = Template("higgsCombine_$asimov.$channel$subchannel.$WC1$WC2$ScanType.$version.$syst.$method.mH120.root")
template_outfilename_2D_stub = Template("_$asimov.$channel$subchannel.$WC1$WC2$ScanType.$version.$syst")
template_fitDiagfilename = Template("fitDiagnostics_${asimov}_FitDiag_Test_Uncertainties_${NTOYS}_Toys.root")

# backgrounds
bkgs_all = ['WW', 'QCD', 'Top', 'WZ', 'DY', 'ZZ', 'VH', 'WJets', 'VG', 'nonprompt', 'VV'] # not including sm

# signals
# copied from: https://github.com/amassiro/AnalyticAnomalousCoupling/blob/master/python/AnomalousCouplingEFTNegative.py
# dimension 6 -- 81 ops
dim6_ops = [
    'cG', 'cGtil', 'cH', 'cHB', 'cHBtil', 'cHDD', 'cHG', 'cHGtil',
    'cHW', 'cHWB', 'cHWBtil', 'cHWtil', 'cHbox', 'cHd', 'cHe', 'cHl1',
    'cHl3', 'cHq1', 'cHq3', 'cHu', 'cHudAbs', 'cHudPh', 'cW', 'cWtil',
    'cdBAbs', 'cdBPh', 'cdGAbs', 'cdGPh', 'cdHAbs', 'cdHPh', 'cdWAbs', 'cdWPh',
    'cdd', 'cdd1', 'ceBAbs', 'ceBPh', 'ceHAbs', 'ceHPh', 'ceWAbs', 'ceWPh',
    'ced', 'cee', 'ceu', 'cld', 'cle', 'cledqAbs', 'cledqPh', 'clequ1Abs',
    'clequ1Ph', 'clequ3Abs', 'clequ3Ph', 'cll', 'cll1', 'clq1', 'clq3', 'clu',
    'cqd1', 'cqd8', 'cqe', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'cqu1',
    'cqu8', 'cquqd1Abs', 'cquqd1Ph', 'cquqd8Abs', 'cquqd8Ph', 'cuBAbs', 'cuBPh', 'cuGAbs',
    'cuGPh', 'cuHAbs', 'cuHPh', 'cuWAbs', 'cuWPh', 'cud1', 'cud8', 'cuu',
    'cuu1'
]

WC_pretty_print_dict = {
    # dim6
    'cW': r'$C_W$',
    'cHq3': r'$C_{Hq3}$',
    'cHq1': r'$C_{Hq1}$',
    'cHu': r'$C_{Hu}$',
    'cHd': r'$C_{Hd}$',
    'cHW': r'$C_{HW}$',
    'cHB': r'$C_{HB}$',
    'cHWB': r'$C_{HWB}$',
    'cHl3': r'$C_{Hl3}$',
    'cll1': r'$C_{ll1}$',
    'cHbox': r'$C_{H\square}$',
    'cHDD': r'$C_{HDD}$',
    # dim6 (old)
    'cT0': r'$f_{T0}$',
    'cM0': r'$f_{M0}$',
    # dim8
    'FS0': r'$f_{S,0}$',
    'FS1': r'$f_{S,1}$',
    'FS2': r'$f_{S,2}$',
    'FM0': r'$f_{M,0}$',
    'FM1': r'$f_{M,1}$',
    'FM2': r'$f_{M,2}$',
    'FM3': r'$f_{M,3}$',
    'FM4': r'$f_{M,4}$',
    'FM5': r'$f_{M,5}$',
    'FM6': r'$f_{M,6}$', # not in final analysis
    'FM7': r'$f_{M,7}$',
    'FT0': r'$f_{T,0}$',
    'FT1': r'$f_{T,1}$',
    'FT2': r'$f_{T,2}$',
    'FT3': r'$f_{T,3}$',
    'FT4': r'$f_{T,4}$',
    'FT5': r'$f_{T,5}$',
    'FT6': r'$f_{T,6}$',
    'FT7': r'$f_{T,7}$',
    'FT8': r'$f_{T,8}$',
    'FT9': r'$f_{T,9}$',
}

WC_pretty_print_dict_AN = {
    # dim6
    'cW': r'$c_W$',
    'cHq3': r'$c_{Hq3}$',
    'cHq1': r'$c_{Hq1}$',
    'cHu': r'$c_{Hu}$',
    'cHd': r'$c_{Hd}$',
    'cHW': r'$c_{HW}$',
    'cHB': r'$c_{HB}$',
    'cHWB': r'$c_{HWB}$',
    'cHl3': r'$c_{Hl3}$',
    'cll1': r'$c_{ll1}$',
    'cHbox': r'$c_{H\square}$',
    'cHDD': r'$c_{HDD}$',
    # dim6 (old)
    'cT0': r'$f_{T0}$',
    'cM0': r'$f_{M0}$',
    # dim8
    'FS0': r'$f_{S,0}$',
    'FS1': r'$f_{S,1}$',
    'FS2': r'$f_{S,2}$',
    'FM0': r'$f_{M,0}$',
    'FM1': r'$f_{M,1}$',
    'FM2': r'$f_{M,2}$',
    'FM3': r'$f_{M,3}$',
    'FM4': r'$f_{M,4}$',
    'FM5': r'$f_{M,5}$',
    'FM6': r'$f_{M,6}$', # not in final analysis
    'FM7': r'$f_{M,7}$',
    'FT0': r'$f_{T,0}$',
    'FT1': r'$f_{T,1}$',
    'FT2': r'$f_{T,2}$',
    'FT3': r'$f_{T,3}$',
    'FT4': r'$f_{T,4}$',
    'FT5': r'$f_{T,5}$',
    'FT6': r'$f_{T,6}$',
    'FT7': r'$f_{T,7}$',
    'FT8': r'$f_{T,8}$',
    'FT9': r'$f_{T,9}$',
}

# aliases defined for paper
WC_pretty_print_dict_paper = {
    # dim6
    'cW': r'\cW',
    'cHq3': r'\cHqthree',
    'cHq1': r'\cHqone',
    'cHu': r'\cHu',
    'cHd': r'\cHd',
    'cHW': r'\cHW',
    'cHB': r'\cHB',
    'cHWB': r'\cHWB',
    'cHl3': r'\cHlthree',
    'cll1': r'\cllone',
    'cHbox': r'\cHsquare',
    'cHDD': r'\cHDD',
    # dim6 (old)
    'cT0': r'\fT{0}',
    'cM0': r'\fM{0}',
    # dim8
    'FS0': r'\fS{0}',
    'FS1': r'\fS{1}',
    'FS2': r'\fS{2}',
    'FM0': r'\fM{0}',
    'FM1': r'\fM{1}',
    'FM2': r'\fM{2}',
    'FM3': r'\fM{3}',
    'FM4': r'\fM{4}',
    'FM5': r'\fM{5}',
    'FM6': r'\fM{6}', # not in final analysis
    'FM7': r'\fM{7}',
    'FT0': r'\fT{0}',
    'FT1': r'\fT{1}',
    'FT2': r'\fT{2}',
    'FT3': r'\fT{3}',
    'FT4': r'\fT{4}',
    'FT5': r'\fT{5}',
    'FT6': r'\fT{6}',
    'FT7': r'\fT{7}',
    'FT8': r'\fT{8}',
    'FT9': r'\fT{9}',
}

SR_pretty_print_dict_AN = {
    # subchannel file names
    '0L_2FJ': r'SR-0l-2fj',
    '0L_3FJ': r'SR-0l-3fj',
    '1L_2FJ': r'SR-\ensuremath{\ell}-2fj',
    '2L_OS_OF': r'SR-2l-OSOF-1fj',
    '2L_OS_SFZ': r'SR-2l-OSonZ-1fj',
    '2L_OS_SFnoZ': r'SR-2l-OSoffZ-1fj',
    '2L_OS_2FJ': r'SR-2l-OS-2fj',
    '2L_SS_1FJ': r'SR-2l-SS-1fj',
    # tau channels to be confirmed
    '0L_2FJ_1T': r'SR-1T-0l-2fj',
    '1L_1FJ_1T': r'SR-1T-1l-1fj',
    '2L_0FJ_1T': r'SR-1T-2l-0fj',
    # additional, e.g. combining 2L_OS
    # to be confirmed
    '2L_OS': r'SR-2l-OS-1fj',
    # copy of 2L_SS
    '2L_SS': r'SR-2l-SS-1fj',
}
