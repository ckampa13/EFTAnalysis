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
    'cT0': r'$f_{T0}$',
    'cM0': r'$f_{M0}$',
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
    'cT0': r'$f_{T0}$',
    'cM0': r'$f_{M0}$',
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
}
