import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename, datacard_dir, dim6_ops

# combine subchannels in a channel
def combine_channel_subchannels(channel, version, datacard_dict, dim, ScanType, StatOnly, SignalInject=False, WC=None, vsuff='', subdir=''):
    version_full = version + vsuff
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: %s; Subchannel: ' % channel
    n_sch_added = 0
    for i, subch in enumerate(subchannels):
        str_ += subch
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            str_ += ' (2018 scaled)'
        tfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version_full, file_type='txt')
        if SignalInject:
            dc_file = os.path.join(dcdir, channel, version, 'signal_injection_'+WC, tfile)
        else:
            dc_file = os.path.join(dcdir, channel, version, subdir, tfile)
        if not os.path.exists(dc_file):
            continue
        dc_name = ' sch%s'% sname_sch
        cmd_str += '%s=%s' % (dc_name, dc_file)
        str_ += ', '
        n_sch_added += 1
    print(str_)
    if n_sch_added < 1:
        print('No channels to add, moving on...\n')
        return
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version=version_full, file_type='txt')
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'channel', tfile_comb)
    cmd_str += ' > '+ comb_file
    #print(cmd_str)
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)

# combine all channels
def combine_all_channels(datacard_dict, dim, ScanType, StatOnly, SignalInject=False, WC=None, vsuff='', subdir=''):
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    channels = datacard_dict.keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: '
    n_ch_added = 0
    n_sch_added = 0
    #for i, ch in enumerate(channels):
    # DEBUG MULTIDIM
    for i, ch in enumerate(['0Lepton_2FJ', '0Lepton_3FJ']):
        # channels may not always have dim8
        has_NDIM = True
        if vsuff == '_NDIM':
            if 'v_NDIM' in versions_dict[ch].keys():
                has_NDIM = True
                WCs_ch = versions_dict[ch]['EFT_ops_NDIM']
            else:
                has_NDIM = False
                #WCs_ch = versions_dict[channel]['EFT_ops']
                WCs_ch = []
        else:
            WCs_ch = versions_dict[ch]['EFT_ops']
        # FIXME! This is a bit misleading. We pass through for 1D files
        # as has_NDIM defaults to True.
        if not has_NDIM:
            continue
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
        version_full = version+vsuff
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
            tfile_ch = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc=SO_lab, version=version_full, file_type='txt')
            if SignalInject:
                dc_file = os.path.join(dcdir, ch, version, 'signal_injection_'+WC, tfile_ch)
            else:
                dc_file = os.path.join(dcdir, ch, version, subdir, tfile_ch)
            if not os.path.exists(dc_file):
                continue
            dc_name = ' ch'+sname_ch+'sch'+sname_sch
            cmd_str += '%s=%s' % (dc_name, dc_file)
            n_sch_added += 1
        str_ += ', '
    print(str_)
    if n_sch_added < 1:
        print('No channels to add, moving on...\n')
        return
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_'+WC
    else:
        suff_purp = ''
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined', WC=dim, ScanType=ScanType, purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='txt')
    comb_file = os.path.join(datacard_dir, 'combined_datacards', 'full_analysis', tfile_comb)
    cmd_str += ' > ' + comb_file
    print(cmd_str)
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-i', '--SignalInject',
                        help='Do you want to use generated signal injection files? If n, default files will be combined. n(default)/y.')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study in the signal injection case? ["cW", ...]')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0", "_NDIM",...]')
    parser.add_argument('-d', '--DCSubDir',
                        help='Subdirectory of the datacard/root files, e.g. for clipping. ["" (default), "clipping",...]')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.SignalInject is None:
        SignalInject = False
    else:
        SignalInject = args.SignalInject == 'y'
    if args.WC is None:
        WC_SI = 'cW'
    else:
        WC_SI = args.WC
    # check if dim6 and dim8 in WC_ALL
    dims = []
    for WC in WC_ALL:
    # for WC in WC_list:
        if WC in dim6_ops:
            dims.append('dim6')
            break
    for WC in WC_ALL:
    # for WC in WC_list:
        if not WC in dim6_ops:
            dims.append('dim8')
            break
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    if args.DCSubDir is None:
        subdir = ''
    else:
        subdir = args.DCSubDir
    #########################
    # outer loop (over EFT dimension)
    for dim in dims:
        print(dim)
        print('=================================================')
        # print('WC: %s' % WC)
        #########################
        # combine channel subchannels
        print('Combining subchannels for each available channel:')
        print('=================================================')
        for channel in channels:
            # channels may not always have dim8
            has_NDIM = True
            if vsuff == '_NDIM':
                if 'v_NDIM' in versions_dict[channel].keys():
                    has_NDIM = True
                    WCs_ch = versions_dict[channel]['EFT_ops_NDIM']
                else:
                    has_NDIM = False
                    #WCs_ch = versions_dict[channel]['EFT_ops']
                    WCs_ch = []
            else:
                WCs_ch = versions_dict[channel]['EFT_ops']
            # FIXME! This is a bit misleading. We pass through for 1D files
            # as has_NDIM defaults to True.
            if not has_NDIM:
                continue
            if dim=='dim8':
                has_dim8 = False
                for WC in WCs_ch:
                    if not WC in dim6_ops:
                        has_dim8 = True
                        break
                if not has_dim8:
                    continue
            # WCs = versions_dict[channel]['EFT_ops']
            # if not WC in WCs:
            #     continue
            if vsuff == '_NDIM':
                v = versions_dict[channel]['v_NDIM']
            else:
                v = versions_dict[channel]['v']
            VERSION = 'v' + str(v)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                combine_channel_subchannels(channel, VERSION, datacard_dict, dim, ScanType=args.ScanType, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC_SI, vsuff=vsuff, subdir=subdir)
        print('=================================================\n')
        #########################
        # combine all channels
        print('Combining all channels (complete analysis):')
        print('=================================================')
        for StatOnly in [False, True]:
            print('Stat only? ', StatOnly)
            combine_all_channels(datacard_dict, dim, ScanType=args.ScanType, StatOnly=StatOnly, SignalInject=SignalInject, WC=WC_SI, vsuff=vsuff, subdir=subdir)
        print('=================================================\n')
        #########################
