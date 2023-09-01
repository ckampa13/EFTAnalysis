import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename, datacard_dir

# combine subchannels in a channel
def combine_channel_subchannels(channel, version, datacard_dict, WC, ScanType, StatOnly, SignalInject=False):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: %s; Subchannel: ' % channel
    for i, subch in enumerate(subchannels):
        str_ += subch
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            str_ += ' (2018 scaled)'
        tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
        if SignalInject:
            dc_file = os.path.join(dcdir, channel, version, 'signal_injection_'+WC, tfile)
        else:
            dc_file = os.path.join(dcdir, channel, version, tfile)
        dc_name = ' sch%s'% sname_sch
        cmd_str += '%s=%s' % (dc_name, dc_file)
        str_ += ', '
    print(str_)
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version=version, file_type='txt')
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'channel', tfile_comb)
    # cmd_str += '> '+ comb_file
    cmd_str += ' > '+ comb_file
    # print(cmd_str)
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)

# combine all channels
def combine_all_channels(datacard_dict, WC, ScanType, StatOnly, SignalInject=False):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    channels = datacard_dict.keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: '
    n_ch_added = 0
    for i, ch in enumerate(channels):
        WCs = versions_dict[ch]['EFT_ops']
        if not WC in WCs:
            continue
        else:
            n_ch_added += 1
        str_ += ch
        v = versions_dict[ch]['v']
        version = 'v' + str(v)
        if versions_dict[ch]['lumi'] == '2018':
            str_ + ' (2018 scaled)'
        sname_ch = datacard_dict[ch]['info']['short_name']
        # loop through subchannels
        subchannels = datacard_dict[ch]['subchannels'].keys()
        for j, subch in enumerate(subchannels):
            sname_sch = datacard_dict[ch]['subchannels'][subch]['info']['short_name']
            # update subchannel name if there is rescaling
            if versions_dict[ch]['lumi'] == '2018':
                sname_sch += '_2018_scaled'
            tfile_ch = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
            if SignalInject:
                dc_file = os.path.join(dcdir, ch, version, 'signal_injection_'+WC, tfile_ch)
            else:
                dc_file = os.path.join(dcdir, ch, version, tfile_ch)
            dc_name = ' ch'+sname_ch+'sch'+sname_sch
            cmd_str += '%s=%s' % (dc_name, dc_file)
        str_ += ', '
    print(str_)
    # stop here if there weren't any WC matches
    if n_ch_added == 0:
        print('No channels have the following WC: '+WC+', combineCards.py will not be run!')
        return
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined', WC=WC, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis', tfile_comb)
    # cmd_str += '> ' + comb_file
    cmd_str += ' > ' + comb_file
    # print(cmd_str)
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW" (default), ...]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_1D" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WC_ALL
    else:
        WCs_loop = [args.WC]
    if args.ScanType is None:
        args.ScanType = '_1D'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    #########################
    # outer loop (over WC)
    for WC in WCs_loop:
        print('WC: %s' % WC)
        #########################
        # combine channel subchannels
        print('Combining subchannels for each available channel:')
        print('=================================================')
        for channel in channels:
            WCs = versions_dict[channel]['EFT_ops']
            if not WC in WCs:
                continue
            v = versions_dict[channel]['v']
            VERSION = 'v' + str(v)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                combine_channel_subchannels(channel, VERSION, datacard_dict, WC=WC, ScanType=args.ScanType, StatOnly=StatOnly, SignalInject=SignalInject)
        print('=================================================\n')
        #########################
        # combine all channels
        print('Combining all channels (complete analysis):')
        print('=================================================')
        for StatOnly in [False, True]:
            print('Stat only? ', StatOnly)
            combine_all_channels(datacard_dict, WC=WC, ScanType=args.ScanType, StatOnly=StatOnly, SignalInject=SignalInject)
        print('=================================================\n')
        #########################
