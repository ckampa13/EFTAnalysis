'''
The bin stat errors don't copy over properly when using uproot. Need to update
them by hand here.
'''

import os
import argparse
import ROOT
import shutil
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from MISC_CONFIGS import datacard_dir

def update_bin_stat_errors(WC, filename_subch, filename_bin, bin_n):
    '''
    Note this function only works for a single bin file -- see SetBinError line
    which assumes we only need to set what is in bin 1.
    '''
    cpfile = os.path.join(datacard_dir, 'output', 'single_bin', 'hold_bin.root')
    # copy file
    shutil.copyfile(filename_bin, cpfile)
    # load files
    fullfile = ROOT.TFile(filename_subch, "read")
    infile = ROOT.TFile(cpfile, "read")
    outfile = ROOT.TFile(filename_bin, "recreate")
    keys_cleaned = [k.GetName() for k in infile.GetListOfKeys() if "TH1" in k.GetClassName()]
    for k in keys_cleaned:
        hin = infile.Get(k)
        hfull = fullfile.Get(k)
        # update any error that isn't EFT or systematics
        if (WC not in k) and ('sm' not in k) and ('Up' not in k) and ('Down' not in k):
            hin.SetBinError(1, hfull.GetBinError(bin_n))
        if ((WC in k) or ('sm' in k)) and (('Up' not in k) and ('Down' not in k)):
            hin.SetBinError(1, 0.0)
        outfile.WriteObject(hin, k)
    # close files
    fullfile.Close()
    infile.Close()
    outfile.Close()
    # delete copied file
    os.remove(cpfile)

if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-fs', '--FileSubChannel',
                        help='Name of subchannel ROOT file (including full path!).')
    parser.add_argument('-fb', '--FileBin',
                        help='Name of bin ROOT file (including full path!).')
    parser.add_argument('-b', '--BinNum',
                        help='Bin number (should match ROOT file name). [1 (default),...]')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["cW" (default),]')
    args = parser.parse_args()
    # fill defauls if necessary
    if args.WC is None:
        args.WC = 'cW'
    if args.BinNum is None:
        args.BinNum = '1'
    # run function
    update_bin_stat_errors(args.WC, args.FileSubChannel, args.FileBin, int(args.BinNum))
