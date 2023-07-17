'''
Create single bin ROOT files.

NOTE: Auto-fills "-1" in observation line of datacard (so this will come from the "h_data_obs" histogram).

This script should be run using miniconda VVV environment (needs uproot).
'''
import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir

stat_script = os.path.join(datacard_dir, 'scripts', 'tools', 'update_bin_stat_errors.py')

# generic function
def update_func(channel, subchannel, ddir, fname):
    fname_subch = os.path.join(ddir, fname)
    # how many bins?
    bins = datacard_dict[channel]['subchannels'][subchannel]['bins']
    for i, bin_n in enumerate(bins):
        # updated file name
        dc_file_bin = fname.split('.')
        dc_file_bin[1] = dc_file_bin[1] + '_bin'+str(bin_n)
        dc_file_bin = os.path.join(ddir, '.'.join(dc_file_bin))
        # run stat error update script
        cmd_str = 'python '+stat_script+' -fs '+fname_subch+' -fb '+ dc_file_bin \
            + ' -b '+str(bin_n)+' -c '+channel
        # TESTING
        # print(cmd_str)
        _ = subprocess.run(cmd_str, shell=True, stdout=None)

# update subchannels in a channel
def update_channel_subchannels(channel, version, datacard_dict):
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    print(f'Channel: {channel}; Subchannel: ', end='')
    for i, subch in enumerate(subchannels):
        if i == (len(subchannels)-1):
            print(subch, end='')
        else:
            print(subch,', ', end='')
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        tfile = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned', version=version, file_type='root')
        # dc_file = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
        # dc_file = os.path.join(dcdir, channel, version, tfile)
        # run helper functions
        dir_ = os.path.join(dcdir, channel, version)
        update_func(channel, subch, dir_, tfile)
    print()


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help=f'Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    # parser.add_argument('-w', '--WC',
    #                     help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default),]')
    # parser.add_argument('-s', '--ScanType',
    #                     help=f'What type of EFT scan was included in this file? ["_1D" (default),]')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    # if args.WC is None:
    #     args.WC = 'cW'
    # if args.ScanType is None:
    #     args.ScanType = '_1D'
    #########################
    # split channel subchannels
    print('Updating bin errors for all subchannels in each available channel:')
    print('=================================================')
    # for channel in datacard_dict.keys():
    for channel in channels:
        # check in WC available
        # if args.WC not in versions_dict[channel]['EFT_ops']:
        #     continue
        v = versions_dict[channel]['v']
        VERSION = f'v{v}'
        update_channel_subchannels(channel, VERSION, datacard_dict)
    print('=================================================\n')
    #########################
