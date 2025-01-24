import os
import subprocess
import argparse
import numpy as np
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename, datacard_dir, dim6_ops

# combine all channels
# def combine_all_channels_leave_one_out(channel_leave_out, datacard_dict, dim, ScanType, StatOnly, SignalInject=False, WC=None):
def combine_all_channels_leave_one_out(channels_leave_out, datacard_dict, dim, ScanType, StatOnly, SignalInject=False, WC=None, file_suff=None, vsuff='', Unblind=False):
    if type(channels_leave_out) is str:
        print("Caution! 'channels_leave_out' should be a list, not a str. Creating a length 1 list.")
        channels_leave_out = [channels_leave_out]
    if file_suff is None:
        # if type(channels_leave_out) is str:
        #     file_suff = channels_leave_out
        # else:
        #     file_suff = channels_leave_out[0]
        file_suff = channels_leave_out[0]
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    channels = datacard_dict.keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: '
    n_ch_added = 0
    for i, ch in enumerate(channels):
        # if ch == channel_leave_out:
        if ch in channels_leave_out:
            continue
        if Unblind:
            ch_unbl = versions_dict[ch]['unblind']
            if not ch_unbl:
                continue
        # channels may not always have dim8
        WCs_ch = versions_dict[ch]['EFT_ops']
        if dim=='dim8':
            has_dim8 = False
            for WC in WCs_ch:
                if not WC in dim6_ops:
                    has_dim8 = True
                    break
            if not has_dim8:
                continue
        str_ += ch
        if vsuff == '_NDIM':
            v = versions_dict[ch]['v_NDIM']
        else:
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
            tfile_ch = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
            if SignalInject:
                dc_file = os.path.join(dcdir, ch, version, 'signal_injection_'+WC, tfile_ch)
            else:
                dc_file = os.path.join(dcdir, ch, version, tfile_ch)
            dc_name = ' ch'+sname_ch+'sch'+sname_sch
            cmd_str += '%s=%s' % (dc_name, dc_file)
        str_ += ', '
    print(str_)
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    #tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+channel_leave_out, WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+file_suff, WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='txt')
    comb_file = os.path.join(dcdir, 'combined_datacards', 'leave_one_out', tfile_comb)
    cmd_str += ' > ' + comb_file
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel to leave out? ["all" (default, looping), "all_tau" (remove tau channels), "not_tau" (combine tau channels), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for NDIM files. ["" (default), "_NDIM",...]')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()+['all_tau', 'not_tau']
    else:
        channels = [args.Channel]
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    # if args.WC is None:
    #     args.WC = 'cW'
    # check if dim6 and dim8 in WC_ALL
    dims = []
    for WC in WC_ALL:
        if WC in dim6_ops:
            dims.append('dim6')
            break
    for WC in WC_ALL:
        if not WC in dim6_ops:
            dims.append('dim8')
            break
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    #########################
    # outer loop (over EFT dimension)
    for dim in dims:
        print(dim)
        print('=================================================')
        # print('WC: %s' % WC)
        #########################
        # combine channel subchannels
        print('Combining all channels (leave one out):')
        print('=================================================')
        for channel in channels:
            if channel == 'all_tau':
                channels_leave_out = [ch for ch in datacard_dict.keys() if ch[-3:] == '_1T']
                file_suff = 'all_tau'
                print('"all_tau" has the following channels: %s' % channels_leave_out)
            elif channel == 'not_tau':
                channels_leave_out = [ch for ch in datacard_dict.keys() if ch[-3:] != '_1T']
                file_suff = 'not_tau'
                print('"not_tau" has the following channels: %s' % channels_leave_out)
            else:
                channels_leave_out = [channel]
                file_suff = None
            # channels may not always have dim8
            WCs_ch_all = []
            for ch in channels_leave_out:
                WCs_ch = versions_dict[ch]['EFT_ops']
                WCs_ch_all.append(WCs_ch)
            WCs_ch_all = np.concatenate(WCs_ch_all)
            if dim=='dim8':
                has_dim8 = False
                #for WC in WCs_ch:
                for WC in WCs_ch_all:
                    if not WC in dim6_ops:
                        has_dim8 = True
                        break
                if not has_dim8:
                    continue
            # WCs = versions_dict[channel]['EFT_ops']
            # if not WC in WCs:
            #     continue
            #print('Leaving out: ', channel)
            print('Leaving out: ', channels_leave_out)
            # v = versions_dict[channel]['v']
            # VERSION = 'v' + str(v)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                #combine_all_channels_leave_one_out(channel, datacard_dict, dim, ScanType=args.ScanType,
                combine_all_channels_leave_one_out(channels_leave_out, datacard_dict, dim, ScanType=args.ScanType,
                                                   StatOnly=StatOnly, SignalInject=SignalInject, WC=WC, vsuff=vsuff,
                                                   file_suff=file_suff, Unblind=Unblind)
        print('=================================================\n')
        #########################
