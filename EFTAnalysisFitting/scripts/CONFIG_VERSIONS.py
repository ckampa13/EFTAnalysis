# store version of each channel to use when running combine
# also track what integrated luminosity is in that version of the yield file
versions_dict = {
    # '0Lepton_2J': {'v': 1, 'lumi': 'Run2'},
    '0Lepton_3FJ': {'v': 4, 'lumi': 'Run2'},
    # '1Lepton': {'v': 1, 'lumi': 'Run2'},
    '2Lepton_OS': {'v': 2, 'lumi': 'Run2'},
    '2Lepton_SS': {'v': 1, 'lumi': '2018'},
}

L_2018 = 59.83 # fb^-1
L_Run2 = 137.64 # fb^-1
scale_2018_to_Run2 = L_Run2 / L_2018
