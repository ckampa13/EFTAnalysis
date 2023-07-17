# store version of each channel to use when running combine
# also track what integrated luminosity is in that version of the yield file
versions_dict = {
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHDD', 'cHW', 'cHB', 'cHWB']}, # no systematics
    # '0Lepton_2FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not suppressed.
    # '0Lepton_3FJ': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points'},
    # '0Lepton_3FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points'}, # rebinning test, no systematics, more 1D scans
    # '0Lepton_3FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    '0Lepton_3FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHDD', 'cHW', 'cHB', 'cHWB']}, # no systematics
    # '0Lepton_3FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not supressed.
    # '1Lepton': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'points'},
    # '2Lepton_OS': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params'}, # bin error
    # '2Lepton_OS': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params'},
    '2Lepton_OS': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # removed WWZ ggH
    # '2Lepton_SS': {'v': 1, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    '2Lepton_SS': {'v': 2, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1']},
}

WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB']

L_2018 = 59.83 # fb^-1
L_Run2 = 137.64 # fb^-1
scale_2018_to_Run2 = L_Run2 / L_2018
