# 07-08-25, Cole Kampa
# In original version of the code, we assume "full analysis" level files only.

import os
from time import time
import subprocess
import shutil
import argparse
import numpy as np
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, WCs_clip_dim6, WCs_clip_dim8, WCs_NDIM
from MISC_CONFIGS import (
    datacard_dir,
    # template_filename,
    template_outfilename,
    # template_outfilename_stub,
    # dim6_ops,
    # prof_grid_dict,
    # NPs_to_promote_dict,
    # USE_NP_POI_DICT,
)

def make_hadd_cmd(files_in, file_out):
    cmd_str = 'hadd -f ' + file_out + ' ' + ' '.join(files_in)
    print(cmd_str)
    return cmd_str

def find_files_grid(ddir, query_strings):
    files = os.listdir(ddir)
    files_in = []
    for f in files:
        queries = [lfunc(f) for lfunc in query_strings]
        if np.alltrue(queries):
            files_in.append(os.path.join(ddir, f))
    return files_in

if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir',
                        help='Where to search for the grid jobs? Assumes starting point is (unblind): EFTAnalysisFitting/unblind/output/grid/. e.g. "profile/07-07-25". No default.')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["all" (default), "dim6", "dim8", "NDIM", "cW", ...]')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default), "_1D" (freeze WCs)]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "y"(default)/"n".')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WC_ALL
    elif args.WC == 'dim6':
        WCs_loop = dim6_WCs
    elif args.WC == 'dim8':
        WCs_loop = dim8_WCs
    elif args.WC == 'NDIM':
        WCs_loop = WCs_NDIM
    else:
        WCs_loop = [args.WC]
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = 'Asimov'
    else:
        asi_str = 'Data'
    if args.Unblind is None:
        args.Unblind = 'y'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff

    # build datadir (input and output)
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    ddir_stub = os.path.join(dcdir, 'output')
    indir = os.path.join(ddir_stub, 'grid', args.datadir, '')
    outdir = os.path.join(ddir_stub, 'full_analysis', '')
    # extras
    version = 'vCONFIG_VERSIONS'+vsuff
    stdout = subprocess.PIPE
    # loop through WCs
    for WC in WCs_loop:
        print(WC)
        for syst, syst_str in zip([True, False], ['.syst.', '.nosyst.']):
            print('With syst? %s' % syst)
            query_strings = [lambda x: 'higgsCombine_' in x, # make sure it's the right file type
                             lambda x: '.root' in x, # make sure it's the right file type
                             lambda x: 'MultiDimFit' in x, # make sure it's the right file type
                             lambda x: asi_str in x, # data or Asimov
                             lambda x: 'all_combined' in x, # full_analysis
                             lambda x: WC+args.ScanType in x, # WC and scan type
                             lambda x: syst_str in x, # syst string
                             lambda x: version in x, # version
                             ]
            # output filename
            file_out = template_outfilename.substitute(asimov=asi_str, channel='all', subchannel='_combined', WC=WC, ScanType=args.ScanType, version=version, syst=syst_str.replace('.', ''), method='MultiDimFit')
            file_out = os.path.join(outdir, file_out)
            # get input files
            files_in = find_files_grid(indir, query_strings)
            files_in = sorted(files_in)
            if len(files_in) > 0:
                print("Combining %d files..." % len(files_in))
                print("Making output file: %s" % file_out)
                cmd_str = make_hadd_cmd(files_in, file_out)
                # run command
                proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
            else:
                print("No input files found -- nothing to do.")
        print()
    print("Done.")
