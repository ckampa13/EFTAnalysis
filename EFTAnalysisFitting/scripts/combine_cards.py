import os
import subprocess
import argparse
# local imports
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict
from MISC_CONFIGS import template_filename

datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
# output_base = 'output'
# output_sub = 'combined'
# output_dir_base = os.path.join(datacard_dir, output_base, output_sub)
# make paths absolute
datacard_dir = os.path.abspath(datacard_dir)
# output_dir_base = os.path.abspath(output_dir_base)

# DEPRECATED...no longer needed now that ROOT file is automatically combined.
'''
# combine bins in a subchannel
def combine_subchannel_bins(channel, subchannel, version, datacard_dict):
    dcdir = os.path.join(datacard_dir, channel, version)
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    bins = datacard_dict[channel]['subchannels'][subchannel]['bins']
    cmd_str = 'combineCards.py '
    print(f'Channel: {channel}; Subchannel: {subchannel}; Bin: ', end='')
    for i, b in enumerate(bins):
        if i == (len(bins)-1):
            print(b)
        else:
            print(b,', ', end='')
        dc_file = os.path.join(dcdir, f'datacard1opWithBkg_FT0_bin{b}_{fname_ch}{fname_sch}.txt')
        dc_name = f'sch{sname_ch}{sname_sch}_b{b}_{version}'
        cmd_str += f'{dc_name}={dc_file} '
    # construct output file
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'subchannel',
                             f'datacard1opWithBkg_FT0_binAll_{fname_ch}{fname_sch}_{version}.txt')
    cmd_str += f'> {comb_file}'
    # run combine script
    # stdout = subprocess.PIPE
    stdout = None
    proc = subprocess.run(cmd_str, shell=True, stdout=stdout)
'''

# combine subchannels in a channel
def combine_channel_subchannels(channel, version, datacard_dict, WC, ScanType):
    # dcdir = os.path.join(datacard_dir, 'combined_datacards', 'subchannel')
    dcdir = datacard_dir
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    cmd_str = 'combineCards.py '
    print(f'Channel: {channel}; Subchannel: ', end='')
    for i, subch in enumerate(subchannels):
        if i == (len(subchannels)-1):
            print(subch, end='')
        else:
            print(subch,', ', end='')
        fname_sch = datacard_dict[channel]['subchannels'][subch]['info']['file_name']
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, proc='', version=version, file_type='txt')
        dc_file = os.path.join(dcdir, channel, version, tfile)
        dc_name = f'ch{sname_ch}'
        cmd_str += f'{dc_name}={dc_file} '
    print()
    # construct output file
    tfile_comb = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType, proc='', version=version, file_type='txt')
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'channel', tfile_comb)
    cmd_str += f'> {comb_file}'
    # run combine script
    # stdout = subprocess.PIPE
    stdout = None
    proc = subprocess.run(cmd_str, shell=True, stdout=stdout)

# TO UPDATE
# combine all channels
def combine_all_channels(version, datacard_dict):
    dcdir = os.path.join(datacard_dir, 'combined_datacards', 'channel')
    channels = datacard_dict.keys()
    cmd_str = 'combineCards.py '
    print(f'Channel: ', end='')
    for i, ch in enumerate(channels):
        if i == (len(channels)-1):
            print(ch)
        else:
            print(ch,', ', end='')
        fname_ch = datacard_dict[ch]['info']['file_name']
        dc_file = os.path.join(dcdir, f'datacard1opWithBkg_FT0_binAll_{fname_ch}All_{version}.txt')
        dc_name = f'all' # ???
        cmd_str += f'{dc_name}={dc_file} '
    # construct output file
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis',
                             f'datacard1opWithBkg_FT0_binAll_channelsAll_{version}.txt')
    cmd_str += f'> {comb_file}'
    # run combine script
    # stdout = subprocess.PIPE
    stdout = None
    proc = subprocess.run(cmd_str, shell=True, stdout=stdout)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default),]')
    parser.add_argument('-s', '--ScanType',
                        help=f'What type of EFT scan was included in this file? ["_1D" (default),]')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'cW'
    if args.ScanType is None:
        args.ScanType = '_1D'
    # DEPRECATED (versions stored in config)
    # which version of datacards?
    # VERSION = 'v1'
    #########################
    '''
    # combine subchannel bins
    print('Combining bins for each available subchannel:')
    # print('=================================================')
    print('=============================================')
    for channel in datacard_dict.keys():
        for subchannel in datacard_dict[channel]['subchannels'].keys():
            combine_subchannel_bins(channel, subchannel, VERSION, datacard_dict)
    # print('=================================================')
    print('=============================================\n')
    '''
    #########################
    # combine channel subchannels
    print('Combining subchannels for each available channel:')
    print('=================================================')
    for channel in datacard_dict.keys():
        v = versions_dict[channel]['v']
        VERSION = f'v{v}'
        combine_channel_subchannels(channel, VERSION, datacard_dict, WC=args.WC, ScanType=args.ScanType)
    print('=================================================\n')
    '''
    #########################
    # combine all channels
    print('Combining all channels (complete analysis):')
    print('=================================================')
    combine_all_channels(VERSION, datacard_dict, WC=args.WC)
    print('=================================================\n')
    #########################
    '''
