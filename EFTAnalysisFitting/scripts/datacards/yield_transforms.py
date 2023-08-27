import os
import numpy as np
import ROOT

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
sys.path.append(os.path.join(fpath,'..','tools'))
from MISC_CONFIGS import dim6_ops
from root_file_tools import book_and_set_TH1D


# this is for the point scan
def yield_prune_first_pass(root_in, root_out, drop_flags=['VVV', 'WWW', 'WZZ', 'ZZZ'], replacements={}):
    # root_in should be initialized with "read"
    # root_out should be initialized with "recreate"
    # drop_flags is a list that contains any substrings which indicate that histogram can be dropped
    # --> e.g. drop_flags = ['VVV', 'WWW', 'WWZ', 'WZZ', 'ZZZ'] drops the point scan
    #     which isn't needed after the parabola fits
    print('\nFirst pass pruning...')
    keys = [k.GetName().split(';')[0] for k in root_in.GetListOfKeys() if "TH1" in k.GetClassName()]
    hin = root_in.Get(keys[0])
    nbins = hin.GetNbinsX()
    zeros = nbins*[0.]
    bin_edges = np.array([hin.GetBinLowEdge(i+1) for i in range(nbins+1)])
    for k in keys:
        has_drop = False
        for flag in drop_flags:
            if flag in k:
                has_drop = True
                break
        if has_drop:
            continue
        # next clean up the histogram name
        knew = k
        for old, new in replacements.items():
            knew = knew.replace(old, new)
        # finally add renamed histogram to new file
        root_out.WriteObject(root_in.Get(k), knew)
    # check if h_data_obs exists. if not, initialize to zero
    if 'h_data_obs' not in keys:
        book_and_set_TH1D(root_out, 'h_data_obs', zeros, bin_edges, bin_errors=zeros)

def yield_add_WCs_params(WCs, root_out, results_np_dict):
    print('\nAdding EFT parameter histograms...')
    nbins = len(results_np_dict[WCs[0]])
    zeros = nbins*[0.]
    k0 = root_out.GetListOfKeys()[0].GetName()
    hin = root_out.Get(k0)
    bin_edges = np.array([hin.GetBinLowEdge(i+1) for i in range(nbins+1)])
    # find which WC we will use for SM (dim6 and dim8)
    dim6 = None
    dim8 = None
    for WC in WCs:
        if WC in dim6_ops:
            dim6 = WC
            break
    for WC in WCs:
        if not WC in dim6_ops:
            dim8 = WC
            break
    if not dim6 is None:
        sm_vals_dim6 = [result['params']['c0'] for result in results_np_dict[dim6]]
        book_and_set_TH1D(root_out, 'h_sm_dim6', sm_vals_dim6, bin_edges, bin_errors=zeros)
    if not dim8 is None:
        sm_vals_dim8 = [result['params']['c0'] for result in results_np_dict[dim8]]
        book_and_set_TH1D(root_out, 'h_sm_dim8', sm_vals_dim8, bin_edges, bin_errors=zeros)
    # loop through WC and set the quad and sm_lin_quad params
    for WC in WCs:
        if WC in dim6_ops:
            sm_vals = sm_vals_dim6
        else:
            sm_vals = sm_vals_dim8
        quad = [result['params']['c2'] for result in results_np_dict[WC]]
        sm_lin_quad = [sm+result['params']['c1']+result['params']['c2'] for result, sm in zip(results_np_dict[WC], sm_vals)]
        # book hists
        for k, vals in zip(['h_sm_lin_quad_', 'h_quad_'], [sm_lin_quad, quad]):
            book_and_set_TH1D(root_out, k+WC, vals, bin_edges, bin_errors=zeros)

def yield_split_dim6_dim8(WCs, root_in, root_out, root_out_dim8, has_dim8=True):
    print('\nSplitting yield file to dim6 and dim8...')
    keys = [k.GetName().split(';')[0] for k in root_in.GetListOfKeys() if "TH1" in k.GetClassName()]
    nbins = root_in.Get(keys[0]).GetNbinsX()
    for k in keys:
        hin = root_in.Get(k)
        EFT_key = False
        WC_key = None
        dim6_in_key = False
        # dim8_in_key = False
        for WC in WCs:
            if WC in k:
                EFT_key = True
                WC_key = WC
                if WC in dim6_ops:
                    dim6_in_key = True
                # else:
                #     dim8_in_key = True
                break
        if EFT_key:
            if dim6_in_key:
                root_out.WriteObject(hin, k)
            else:
                if not has_dim8:
                    raise ValueError('%s contains %s (dim8), but list of WCs does not contain any dim8.' % (k, WC_key))
                root_out_dim8.WriteObject(hin, k)
        # not EFT related, then goes to both files
        else:
            root_out.WriteObject(hin, k)
            if has_dim8:
                root_out_dim8.WriteObject(hin, k)
    # add SM
    root_out.WriteObject(root_in.Get('h_sm_dim6'), 'h_sm')
    if has_dim8:
        root_out_dim8.WriteObject(root_in.Get('h_sm_dim8'), 'h_sm')
