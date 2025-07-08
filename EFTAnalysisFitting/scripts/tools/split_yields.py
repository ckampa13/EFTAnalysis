'''
Create single bin ROOT files.

NOTE: Auto-fills "-1" in observation line of datacard (so this will come from the "h_data_obs" histogram).

This version removes uproot. The errors are set in this script so split_yields2.sh is no longer needed.
'''
import os
import subprocess
import argparse
import numpy as np
import ROOT
# import uproot
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
sys.path.append(os.path.join(fpath,'..','tools'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir, dim6_ops
from root_file_tools import book_and_set_TH1D

# generic function
def split_func(ddir, fname, sname_sch, dc_files):
    root_in = ROOT.TFile(os.path.join(ddir, fname), 'read')
    keys = [k.GetName().split(';')[0] for k in root_in.GetListOfKeys() if "TH1" in k.GetClassName()]
    hin = root_in.Get(keys[0])
    nbins = hin.GetNbinsX()
    bin_edges = [hin.GetBinLowEdge(i+1) for i in range(nbins+1)]
    for i in range(nbins):
        bin_n = i+1
        # updated file name
        dc_file_bin = fname.split('.')
        dc_file_bin[1] = dc_file_bin[1] + '_bin' + str(bin_n)
        dc_file_bin = os.path.join(ddir, '.'.join(dc_file_bin))
        root_out = ROOT.TFile(dc_file_bin, 'recreate')
        for k in keys:
            hin = root_in.Get(k)
            vals = [hin.GetBinContent(bin_n)]
            errs = [hin.GetBinError(bin_n)]
            # increase val above zero if needed (normalization error)
            if vals[0] < 1e-4:
                vals[0] = 1e-4
            edges = np.array([bin_edges[i], bin_edges[i+1]])
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
def split_channel_subchannels(channel, version, datacard_dict, dims, ScanType, Unblind=False):
    version_dir = version.split('_')[0]
    dcdir = datacard_dir
    if Unblind:
        ch_unbl = versions_dict[channel]['unblind']
        if not ch_unbl:
            print('Channel %s is not unblinded, skipping!' % channel)
            return
        dcdir = os.path.join(dcdir, 'unblind')
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    str_ = 'Channel: %s; version: %s:' % (channel, version)
    print(str_)
    str_ = ''
    for dim in dims:
        str_ += dim+': '
        if dim == 'dim8':
            suff_proc = '_dim8'
        else:
            suff_proc = ''
        for i, subch in enumerate(subchannels):
            if subch == '':
                str_ += '"", '
            else:
                str_ += subch + ', '
            sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
            # update subchannel name if there is rescaling
            if versions_dict[channel]['lumi'] == '2018':
                sname_sch += '_2018_scaled'
                str_ += ' (2018 scaled)'
            tfile = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_MultiDimCleaned'+suff_proc, version=version, file_type='root')
            dc_file = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanType, purpose='DataCard_Yields', proc='', version=version, file_type='txt')
            dc_files = [dc_file]
            # run helper functions
            dir_ = os.path.join(dcdir, channel, version_dir)
            # split to new ROOT files for each bin and make a new dc file for each
            split_func(dir_, tfile, sname_sch, dc_files)
        str_ += '\n'
    print(str_)

if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-d', '--Dimension',
                        help='Which dim of EFT ops to process? "all" (default), "dim6", "dim8"')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.Dimension is None:
        args.Dimension = 'all'
    if args.Dimension == 'all':
        dims = ['dim6', 'dim8']
    elif args.Dimension == 'dim6':
        dims = ['dim6']
    elif args.Dimension == 'dim8':
        dims = ['dim8']
    else:
        raise ValueError('The input args.Dimension="%s" is not implemented. Please select from: ["all", "dim6", "dim8"].' % args.Dimension)
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    #########################
    # split channel subchannels
    print('Splitting subchannels into single bins for each available channel:')
    print('=================================================')
    for channel in channels:
        WCs = versions_dict[channel]['EFT_ops']
        # check which dims are in the samples
        # dims = []
        # # dim6
        # for WC in WCs:
        #     if WC in dim6_ops:
        #         dims.append('dim6')
        #         break
        # # dim8
        # for WC in WCs:
        #     if not WC in dim6_ops:
        #         dims.append('dim8')
        #         break
        v = versions_dict[channel]['v']
        VERSION = 'v' + str(v) + vsuff
        split_channel_subchannels(channel, VERSION, datacard_dict, dims, ScanType=args.ScanType,
                                  Unblind=Unblind)
    print('=================================================\n')
    #########################
