# store version of each channel to use when running combine
# also track what integrated luminosity is in that version of the yield file
versions_dict = {
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHDD', 'cHW', 'cHB', 'cHWB']}, # no systematics
    # '0Lepton_2FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not suppressed.
    # '0Lepton_2FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_2FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_2FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updates.
    # '0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    '0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    # '0Lepton_3FJ': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points'},
    # '0Lepton_3FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points'}, # rebinning test, no systematics, more 1D scans
    # '0Lepton_3FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_3FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not supressed.
    # '0Lepton_3FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_3FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_3FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updatees.
    # '0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    '0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    # '1Lepton': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '1Lepton': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # cW -> VVV+1Jet, all other dim6 added. autoMCStats should be turned off.
    '1Lepton': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # All dim8 added (dim6 bugged). Processed only FT0, FM0. autoMCStats should be turned off.
    # '2Lepton_OS': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params'}, # bin error
    # '2Lepton_OS': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params'},
    #'2Lepton_OS': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # removed WWZ ggH
    # '2Lepton_OS': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # signal xsec bug fix
    # '2Lepton_OS': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # 1Jet sample processed
    # '2Lepton_OS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 completed, with minor errors in point scans (removed points)
    '2Lepton_OS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8 completed (FT0, FM0), dim6 completed (with bugged points fixed)
    # '2Lepton_SS': {'v': 1, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '2Lepton_SS': {'v': 2, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1']}, # only WWW
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # VVV, but only cW -- first batch
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # VVV 1J
    '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # VVV 1J, same as previous line with dim8 added.
}

# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB'] # 2L_SS v2
# WC_ALL = ['cW', 'cHDD', 'cHW', 'cHWB', 'cHB'] # 2L_SS v3 -- first batch
# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd'] # full set of dim-6
WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0'] # full set of dim-6, a few representative dim-8

L_2018 = 59.83 # fb^-1
L_Run2 = 137.64 # fb^-1
scale_2018_to_Run2 = L_Run2 / L_2018
