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
                },
            },
            'muon': {
                'bins': [1, 2, 3, 4],
                'info': {
                    'short_name': 'mu',
                    'file_name': 'muon',
                },
            },
        },
        'info': {
            'short_name': '1L',
            'file_name': '1lepton',
        }
    }
}
