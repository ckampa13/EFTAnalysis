import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir, dim6_ops

# combine all channels
def combine_all_channels(datacard_dict, data_suff='_Data', Unblind=True):
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    channels = datacard_dict.keys()
    cmd_str = 'combineCards.py'
    str_ = 'Channel: '
    n_ch_added = 0
    n_sch_added = 0
    for i, ch in enumerate(channels):
    # ALL
    # for i, ch in enumerate(['0Lepton_2FJ', '0Lepton_3FJ', '1Lepton', '2Lepton_SS', '2Lepton_OS_2FJ', '1Lepton_1T', '2Lepton_1T', '2Lepton_OS']):
        if Unblind:
            ch_unbl = versions_dict[ch]['unblind']
            if not ch_unbl:
                continue
        str_ += ch
        v = versions_dict[ch]['v_TEMPLATE']
        version = 'v' + str(v)
        version_full = version
        sname_ch = datacard_dict[ch]['info']['short_name']
        # loop through subchannels
        subchannels = datacard_dict[ch]['subchannels'].keys()
        for j, subch in enumerate(subchannels):
            sname_sch = datacard_dict[ch]['subchannels'][subch]['info']['short_name']
            # update subchannel name if there is rescaling
            tfile_ch = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Templates', proc=data_suff, version=version_full, file_type='txt')
            dc_file = os.path.join(dcdir, ch, version, tfile_ch)
            # DEBUG
            # print(dc_file)
            if not os.path.exists(dc_file):
                # DEBUG
                # print('Does not exist!')
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
    tfile_comb = template_filename_yields.substitute(channel='all', subchannel='_combined', purpose='DataCard_Templates', proc=data_suff, version='vCONFIG_VERSIONS', file_type='txt')
    comb_file = os.path.join(dcdir, 'combined_datacards', 'full_analysis', tfile_comb)
    cmd_str += ' > ' + comb_file
    print(cmd_str)
    # run combine script
    stdout = None
    proc = subprocess.call(cmd_str, shell=True, stdout=stdout)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--DataSuff',
                        help='String to append after "DataCard_Templates" to refer to different entries into "h_data_obs". ["all" (default), "_Data", "_Asimov_cW_1p0", "_Asimov_cHq3_1p0", "_Asimov_sm"]')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "y"(default)/"n".')
    args = parser.parse_args()
    # list of data file
    if args.DataSuff is None:
        args.DataSuff = 'all'
    if args.DataSuff == 'all':
        data_suff_loop = ["_Data", "_Asimov_cW_1p0", "_Asimov_cHq3_1p0", "_Asimov_sm"]
    else:
        data_suff_loop = [args.DataSuff]
    if args.Unblind is None:
        args.Unblind = 'y'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    #########################
    # outer loop (over data suff)
    for data_suff in data_suff_loop:
        print('data_suff = %s' % data_suff)
        print('=================================================')
        #########################
        # combine all channels
        print('Combining all channels (complete analysis):')
        print('=================================================')
        combine_all_channels(datacard_dict, data_suff=data_suff, Unblind=Unblind)
        print('=================================================\n')
        #########################
