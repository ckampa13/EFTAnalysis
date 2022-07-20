'''
Nested dictionary structure:
- Channel (dict)
    + Subchannel (dict)
        * list of bins
'''

datacard_dict = {
    # channel 1
    '1Lepton': {
        'subchannels': {
            'electron': {
                'bins': [1, 2, 3, 4],
                'info': {
                    'short_name': 'e',
                    'file_name': 'electron',
                    'ylabel_name': r'1 Lepton, $e$',
                },
            },
            'muon': {
                'bins': [1, 2, 3, 4],
                'info': {
                    'short_name': 'mu',
                    'file_name': 'muon',
                    'ylabel_name': r'1 Lepton, $\mu$',
                },
            },
        },
        'info': {
            'short_name': '1L',
            'file_name': '1lepton',
            'variable_of_choice': r'$\mathrm{M}_{\mathrm{JJl}\nu}$',
            'ylabel_name': '1 Lepton           \n(2 boosted jets)',
        }
    }
}
