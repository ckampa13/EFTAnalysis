'''
Makes all workspaces at the bin-by-bin, subchannel, channel, full analysis levels.
To make sure up to date datacards and ROOT yield files are used, please ensure
scripts/tools/combine_cards.py and scripts/tools/split_yields.py have both been
run.

In the current version, only single WC are supported.
'''
import os
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, WCs_clip_dim6, WCs_clip_dim8
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir, dim6_ops

str_phys_model = '-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel'

# get mu parameters in the analysis
def get_mu_params(dcfile):
    with open(dcfile, 'r') as f:
        lines = f.readlines()
    lines_procs = []
    for line in lines:
        if "process" in line and "mVVV_b" in line:
            lines_procs.append(line)
    if len(lines_procs) < 1:
        raise ValueError('Could not find process line in the datacard file %s! (Should start with "process" and contain e.g. "mu_mVVV_b1")' % dcfile)
    line_proc = lines_procs[0]
    mu_list = sorted([l for l in list(set(line_proc.split(' '))) if 'mu_mVVV' in l])
    return mu_list

def make_map_str_mu_param(mu, val_def=1, val_min=-10, val_max=20):
    map_str = "--PO 'map=.*/%s:r_%s[%d,%d,%d]'" % (mu, mu, val_def, val_min, val_max)
    return map_str

def make_all_mu_map_strs(mu_list, val_def=1, val_min=-10, val_max=20):
    map_str_list = []
    for mu in mu_list:
        map_str = make_map_str_mu_param(mu, val_def, val_min, val_max)
        map_str_list.append(map_str)
    out_str = ' '.join(map_str_list)
    return out_str

# full analysis
def make_workspace_full_analysis(data_suff, verbose=1, Unblind=True):
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    comb_dcdir = os.path.join(dcdir, 'combined_datacards', 'full_analysis')
    tfile_comb = template_filename_yields.substitute(channel='all', subchannel='_combined', purpose='DataCard_Templates', proc=data_suff, version='vCONFIG_VERSIONS', file_type='txt')
    dc_file = os.path.join(comb_dcdir, tfile_comb)
    print('Full Analysis')
    mu_list = get_mu_params(dc_file)
    print('Found mu signal strength params in %s:' % dc_file)
    print(mu_list)
    cmd_str = 'text2workspace.py '
    cmd_str += '%s %s ' % (dc_file, str_phys_model)
    wsfile = template_filename_yields.substitute(channel='all', subchannel='_combined', purpose='workspace_Templates', proc=data_suff, version='vCONFIG_VERSIONS', file_type='root')
    wsfile = os.path.join(dcdir, 'workspaces', 'full_analysis', wsfile)
    cmd_str += '-o %s ' % wsfile
    # add signal strengths
    # FIXME! I don't think I want range hard coded
    map_out_str = make_all_mu_map_strs(mu_list, val_def=1, val_min=-10, val_max=20)
    cmd_str += map_out_str
    # add SM as a signal?
    cmd_str += " --PO 'map=.*/sm:r_sm[1,0,3]'"
    # add bkg as a signal?
    # cmd_str += " --PO 'map=.*/bkg:r_bkg[1,0,3]'"
    # run script
    if verbose > 0:
        # stdout = None
        stdout = subprocess.PIPE
    else:
        # stdout = subprocess.PIPE
        stdout = None
    if verbose > 0:
        print('generating workspace...')
        print(cmd_str)
    _ = subprocess.call(cmd_str, shell=True, stdout=stdout)
    if verbose > 0:
        print('\ndone.\n')
    else:
        print()


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--DataSuff',
                        help='String to append after "DataCard_Templates" to refer to different entries into "h_data_obs". ["all" (default), "_Data", "_Asimov_cW_1p0", "_Asimov_cHq3_1p0", "_Asimov_sm"]')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-V', '--Verbose',
                        help='Include "combine" output? 0 (default) / 1. "combine" output included if Verbose>0. Beware: Verbose>0 can cause hanging process!')
    args = parser.parse_args()
    # list of data file
    if args.DataSuff is None:
        args.DataSuff = 'all'
    if args.DataSuff == 'all':
        data_suff_loop = ["_Data", "_Asimov_cW_1p0", "_Asimov_cHq3_1p0", "_Asimov_sm"]
    else:
        data_suff_loop = [args.DataSuff]
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    if args.Verbose is None:
        args.Verbose = 0
    else:
        args.Verbose = int(args.Verbose)
    #########################
    # outer loop (over data suff)
    for data_suff in data_suff_loop:
        print('data_suff = %s' % data_suff)
        print('=================================================')
        #########################
        # full analysis workspace
        print('Generating full analysis workspace:')
        print('=================================================')
        make_workspace_full_analysis(data_suff, verbose=args.Verbose, Unblind=Unblind)
        print('=================================================\n')
        #########################
