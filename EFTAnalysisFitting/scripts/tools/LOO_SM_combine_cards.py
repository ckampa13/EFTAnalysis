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

# combine all channels
# def combine_all_channels(datacard_dict, StatOnly, SignalInject=False):
def combine_all_channels_leave_one_out(channels_leave_out, datacard_dict, StatOnly, file_suff=None, Unblind=False):
    if type(channels_leave_out) is str:
        print("Caution! 'channels_leave_out' should be a list, not a str. Creating a length 1 list.")
        channels_leave_out = [channels_leave_out]
    if file_suff is None:
        file_suff = channels_leave_out[0]
    # FIXME! remove SignalInject completely.
    SignalInject=False
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
        if ch in channels_leave_out:
            continue
        if Unblind:
            ch_unbl = versions_dict[ch]['unblind']
            if not ch_unbl:
                continue
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
            tfile_ch = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC='REMOVE', ScanType='', purpose='DataCard_Yields', proc=SO_lab, version=version, file_type='txt')
            tfile_ch = tfile_ch.replace('VVV.', 'SM.').replace('.REMOVE.', '.')
            if SignalInject:
                dc_file = os.path.join(dcdir, ch, version, 'signal_injection_sm', tfile_ch)
            else:
                dc_file = os.path.join(dcdir, ch, version, tfile_ch)
            dc_name = ' ch'+sname_ch+'sch'+sname_sch
            cmd_str += '%s=%s' % (dc_name, dc_file)
        str_ += ', '
    print(str_)
    # construct output file
    if SignalInject:
        suff_purp = '_SignalInject_sm'
    else:
        suff_purp = ''
    version = 'vCONFIG_VERSIONS'
    # tfile_comb = template_filename.substitute(channel='all', subchannel='_combined', WC='REMOVE', ScanType='', purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version=version, file_type='txt')
    tfile_comb = template_filename.substitute(channel='all', subchannel='_combined_LOO_'+file_suff, WC='REMOVE', ScanType='', purpose='DataCard_Yields'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS', file_type='txt')
    tfile_comb = tfile_comb.replace('VVV.', 'SM.').replace('.REMOVE.', '.')
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
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()+['all_tau', 'not_tau']
    else:
        channels = [args.Channel]
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    #########################
    # outer loop (over EFT dimension)
    # for dim in dims:
    for sig in ['sm']:
        # print(dim)
        print(sig)
        print('=================================================')
        # print('WC: %s' % WC)
        #########################
        # combine all channels
        print('Combining all channels (complete analysis):')
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
            print('Leaving out: ', channels_leave_out)
            for StatOnly in [False, True]:
                print('Stat only? ', StatOnly)
                combine_all_channels_leave_one_out(channels_leave_out,
                                     datacard_dict, StatOnly=StatOnly,
                                     file_suff=file_suff, Unblind=Unblind)
        print('=================================================\n')
        #########################
