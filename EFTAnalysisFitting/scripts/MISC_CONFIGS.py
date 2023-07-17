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
