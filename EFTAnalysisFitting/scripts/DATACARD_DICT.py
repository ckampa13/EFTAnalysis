'''
Nested dictionary structure:
- Channel (dict)
    + Subchannel (dict)
        * list of bins
'''

datacard_dict = {
    # channel 0
    '0Lepton': {
        'subchannels': {
            '': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '',
                    'file_name': '',
                    'ylabel_name': r'0 Lepton, 2 Jet',
                }
            }
        },
        'info': {
            'short_name': '0L',
            'file_name': '0Lep',
            'variable_of_choice': r'$\mathrm{H}_{\mathrm{T}}$',
            'ylabel_name': '0 Lepton              \n(2 boosted jets)   ',
        }
    },
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
            'ylabel_name': '1 Lepton              \n(2 boosted jets)   ',
        }
    },
    # channel 2
    '2OSLepton': {
        'subchannels': {
            'OF': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': 'OF',
                    'file_name': '1Jet_OF',
                    'ylabel_name': r'2 OS Lepton, OF',
                },
            },
            'SFnoZ': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': 'SFnoZ',
                    'file_name': '1Jet_SFnoZ',
                    'ylabel_name': '2 OS Lepton,\nSF (no Z)',
                },
            },
            '2FatJets': {
                'bins': [1, 2],
                'info': {
                    'short_name': '2FatJets',
                    'file_name': '2FatJets',
                    'ylabel_name': '2 OS Lepton,\n2 FatJet',
                },
            },
        },
        'info': {
            'short_name': '2OSL',
            'file_name': 'OS',
            'variable_of_choice': r'$\mathrm{s}_{\mathrm{T}}$',
            'ylabel_name': '2 Leptons            \n(opposite signed)',
        }
    },
    # channel 3
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
            'ylabel_name': '2 Leptons            \n(same signed)     ',
        }
    },
    # channel 4 -- may remove?
    # THIS IS A SKETCH IN CASE WE WANT TO ADD THIS AS IT'S OWN CHANNEL
    # '2OSLepton2J': {
    #     'subchannels': {
    #         '': {
    #             'bins': [1, 2],
    #             'info': {
    #                 'short_name': '',
    #                 'file_name': '',
    #                 'ylabel_name': '2 OS Lepton,\n2 FatJet',
    #             },
    #         },
    #     },
    #     'info': {
    #         'short_name': '2OSL2FJ',
    #         'file_name': 'OS2FatJets',
    #         'variable_of_choice': r'$\mathrm{s}_{\mathrm{T}}$',
    #         'ylabel_name': '2 Leptons            \n(opposite signed)',
    #     }
    # },
}
