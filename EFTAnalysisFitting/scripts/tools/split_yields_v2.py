'''
Create single bin ROOT files.

NOTE: Auto-fills "-1" in observation line of datacard (so this will come from the "h_data_obs" histogram).

This version removes uproot. The errors are set in this script so split_yields2.sh is no longer needed.
'''
import os
import subprocess
import argparse
import ROOT
# import uproot
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir, dim6_ops
from tools.root_file_tools import book_and_set_TH1D

# generic function
def split_func(ddir, fname, sname_sch, dc_files):
    root_in = ROOT.TFile(os.path.join(ddir, fname), 'read')
    keys = [k.GetName().split(';')[0] for k in root_in.GetListOfKeys() if "TH1" in k.GetClassName()]
    hin = root_in.Get(keys[0])
    nbins = hin.GetNbinsX()
    # zeros = nbins*[0.]
    bin_edges = np.array([hin.GetBinLowEdge(i+1) for i in range(nbins+1)])
    for i in range(nbins):
        bin_n = i+1
        # updated file name
        dc_file_bin = fname.split('.')
        dc_file_bin[1] = dc_file_bin[1] + '_bin' + str(bin_n)
        dc_file_bin = os.path.join(ddir, '.'.join(dc_file_bin))
        root_out = ROOT.TFile(dc_file_bin, 'recreate')
        for k in keys:
            hin = root_in.Get(k)
            #n, bin_edges = dc_upr[k].to_numpy()
            #n_new = n[i:i+1]
            vals = [hin.GetBinContent(bin_n)]
            errs = [hin.GetBinError(bin_n)]
            # increase val above zero if needed (normalization error)
            if vals[0] < 1e-4:
                vals[0] = 1e-4
            edges = [bin_edges[i], bin_edges[i+1]]
            book_and_set_TH1D(root_out, k, vals, edges, bin_errors=errs)
        # close bin file
        root_out.Close()
        # also want to update the datacard for each WC
        for dc_file in dc_files:
            for StatOnly, SO_str in zip([False, True], ['', '_StatOnly']):
                dc_file_ = dc_file.replace('DataCard_Yields', 'DataCard_Yields' + SO_str)
                update_datacard(ddir, dc_file_, bin_n)
    # close full file
    root_in.Close()

# new datacard
def update_datacard(ddir, dc_name, bin_n):
    # create new datacard file name
    dc_new = dc_name.split('.')
    dc_new[1] = dc_new[1] + '_bin' + str(bin_n)
    dc_new = '.'.join(dc_new)
    # load contents of full datacard
    with open(os.path.join(ddir, dc_name), 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    # create new file, updating the root file lines
    with open(os.path.join(ddir, dc_new), 'w') as f:
        for line in lines:
            if line[:6] == 'shapes':
                line_new = line.split('.')
                line_new[1] = line_new[1] + '_bin' + str(bin_n)
                line_new = '.'.join(line_new)
            elif line[:11] == 'observation':
                line_new = 'observation -1'
            else:
                line_new = line
            f.write(line_new+'\n')

# split subchannels in a channel
def split_channel_subchannels(channel, version, datacard_dict, WCs, ScanType):
    # check if dim8 available
    has_dim8 = False
    for WC in versions_dict[channel]['EFT_ops']:
        if not WC in dim6_ops:
            has_dim8 = True
    dcdir = datacard_dir
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    str_ = 'Channel: %s; version: %s; Subchannel: \n' % (channel, version)
    print(str_)
    str_ = ''
    #print(f'Channel: {channel}; version: {version}; Subchannel: ', end='')
    for i, subch in enumerate(subchannels):
        # if i == (len(subchannels)-1):
            #print(subch, end='')
        # else:
            # print(subch,', ', end='')
        str_ += subch
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            #print(' (2018 scaled),', end='')
            str_ += ' (2018 scaled)'
        str_ += ' -- ' + WCs
        #print(WCs, end=', ')
        tfile = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned', version=version, file_type='root')
        if has_dim8:
            tfile_dim8 = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned_dim8', version=version, file_type='root')
        dc_files = []
        dc_files_dim8 = []
        for WC in WCs:
            dc_file = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
            if WC in dim6_ops:
                dc_files.append(dc_file)
            else:
                dc_files_dim8.append(dc_file)
        # dc_file = os.path.join(dcdir, channel, version, tfile)
        # run helper functions
        dir_ = os.path.join(dcdir, channel, version)
        # split to new ROOT files for each bin and make a new dc file for each
        split_func(dir_, tfile, sname_sch, dc_files)
        # dim8
        if has_dim8:
            split_func(dir_, tfile_dim8, sname_sch, dc_files_dim8)
        str_ += '\n'
        print(str_)
    print()


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_1D" (default),]')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.ScanType is None:
        args.ScanType = '_1D'
    #########################
    # split channel subchannels
    print('Splitting subchannels into single bins for each available channel:')
    print('=================================================')
    for channel in channels:
        WCs = versions_dict[channel]['EFT_ops']
        v = versions_dict[channel]['v']
        VERSION = 'v' + str(v)
        split_channel_subchannels(channel, VERSION, datacard_dict, WCs, ScanType=args.ScanType)
    print()
    print('=================================================\n')
    #########################
