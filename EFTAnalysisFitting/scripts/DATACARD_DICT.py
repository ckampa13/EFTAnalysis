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
                    'file_name': '_electron',
                    'ylabel_name': r'1 Lepton, $e$',
                },
            },
            'muon': {
                'bins': [1, 2, 3, 4],
                'info': {
                    'short_name': 'mu',
                    'file_name': '_muon',
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
    },
    # channel 2
    '2SSLepton': {
        'subchannels': {
            '1Jet': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '1J',
                    'file_name': '1Jet',
                    'ylabel_name': r'2 SS Leptons, 1 Jet',
                }
            }
        },
        'info': {
            'short_name': '2SSL',
            'file_name': 'SS',
            'variable_of_choice': r'$\mathrm{s}_{\mathrm{T}}$',
            'ylabel_name': '2 Leptons          \n(same signed)',
        }
    },
}
