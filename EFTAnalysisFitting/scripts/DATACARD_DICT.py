'''
Nested dictionary structure:
- Channel (dict)
    + Subchannel (dict)
        * list of bins
'''

datacard_dict = {
    # channel 0
    # '0Lepton_2J': {
    #     'subchannels': {
    #         '': {
    #             'bins': [1, 2, 3],
    #             'info': {
    #                 'short_name': '',
    #                 'file_name': '',
    #                 'ylabel_name': r'0 Lepton, 2 Jet',
    #             }
    #         }
    #     },
    #     'info': {
    #         'short_name': '0L_2J',
    #         'file_name': '0Lep_2J',
    #         'variable_of_choice': r'$\mathrm{H}_{\mathrm{T}}$',
    #         'ylabel_name': '0 Lepton              \n(2 boosted jets)   ',
    #     }
    # },
    # channel 1
    '0Lepton_3FJ': {
        'subchannels': {
            '': {
                # 'bins': [1, 2, 3, 4], # v4
                'bins': [1, 2, 3, 4, 5, 6], # v6
                'info': {
                    'short_name': '',
                    'file_name': '',
                    'ylabel_name': r'0 Lepton, 3 FatJet',
                }
            }
        },
        'info': {
            'short_name': '0L_3FJ',
            'file_name': '0Lep_3FJ',
            'variable_of_choice': r'$\mathrm{H}_{\mathrm{T, Fat-Jet}}$',
            'ylabel_name': '0 Lepton              \n(3 fat jets)   ',
        }
    },
    # channel 2
    # '1Lepton': {
    #     'subchannels': {
    #         'electron': {
    #             'bins': [1, 2, 3, 4],
    #             'info': {
    #                 'short_name': '_e',
    #                 'file_name': '_electron',
    #                 'ylabel_name': r'1 Lepton, $e$',
    #             },
    #         },
    #         'muon': {
    #             'bins': [1, 2, 3, 4],
    #             'info': {
    #                 'short_name': '_mu',
    #                 'file_name': '_muon',
    #                 'ylabel_name': r'1 Lepton, $\mu$',
    #             },
    #         },
    #     },
    #     'info': {
    #         'short_name': '1L',
    #         'file_name': '1Lepton',
    #         'variable_of_choice': r'$\mathrm{M}_{\mathrm{JJl}\nu}$',
    #         'ylabel_name': '1 Lepton              \n(2 boosted jets)   ',
    #     }
    # },
    # channel 3
    '2Lepton_OS': {
        'subchannels': {
            'OF': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '_OF',
                    'file_name': '1Jet_OF',
                    'ylabel_name': r'2 OS Lepton, OF',
                },
            },
            'SFnoZ': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '_SFnoZ',
                    'file_name': '1Jet_SFnoZ',
                    'ylabel_name': '2 OS Leptons,\nSF (no Z)',
                },
            },
            # '2FatJets': {
            #     'bins': [1, 2],
            #     'info': {
            #         'short_name': '2FatJets',
            #         'file_name': '2FatJets',
            #         'ylabel_name': '2 OS Lepton,\n2 FatJet',
            #     },
            #},
            'SFZ': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '_SFZ',
                    'file_name': '1Jet_SFZ',
                    'ylabel_name': '2 OS Leptons,\nSF (Z)',
                },
            },
        },
        'info': {
            'short_name': '2L_OS',
            'file_name': '2Lep_OS',
            'variable_of_choice': r'$\mathrm{s}_{\mathrm{T}}$',
            'ylabel_name': '2 Leptons            \n(opposite signed)',
        }
    },
    # channel 4
    '2Lepton_SS': {
        'subchannels': {
            '1FJ': {
                'bins': [1, 2, 3],
                'info': {
                    'short_name': '_1FJ',
                    'file_name': '1FatJet',
                    'ylabel_name': r'2 SS Leptons, 1 fat jet',
                }
            }
        },
        'info': {
            'short_name': '2L_SS',
            'file_name': '2Lep_SS',
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
