# import from this file to get limits from an output root file
import numpy as np
import uproot
from scipy.stats import norm

CL_1sigma = 1. - 2.*norm.cdf(-1, loc=0, scale=1)

def get_NLL(root_file, WC='cW'):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array()[1:].tolist())
    Cs = np.array(file_['limit']['k_'+WC].array()[1:].tolist())

    return Cs, NLL

def get_NLL_full(root_file, WC='cW'):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array().tolist())
    Cs = np.array(file_['limit']['k_'+WC].array().tolist())

    return Cs, NLL

def get_lims(CL_list, Cs=None, NLL=None, root_file=None, WC='cW'):
    # load from file, if FT0 & NLL not supplied
    if Cs is None:
        Cs, NLL = get_NLL(root_file, WC)
    # loop through CLs to determine limits
    NLL_cuts = []
    LLs = []
    ULs = []
    Cs_best = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # get rid of nans
        NLL[np.isnan(NLL)] = 1000.
        # find best value for FT0
        imin = np.argmin(NLL)
        C_best = Cs[imin]
        Cs_best.append(C_best)
        # FIXME! do something more clever than this?
        mask_excluded = NLL > NLL_cut
        LL = np.min(Cs[~mask_excluded])
        UL = np.max(Cs[~mask_excluded])
        LLs.append(LL)
        ULs.append(UL)
    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    LLs = np.array(LLs)
    ULs = np.array(ULs)
    Cs_best = np.array(Cs_best)
    return Cs, NLL, CL_list, NLL_cuts, LLs, ULs

def get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=None, WC='cW'):
    # load from file, if FT0 & NLL not supplied
    if Cs is None:
        Cs, NLL = get_NLL_full(root_file, WC)
        C_best = Cs[0]
        NLL_best = NLL[0]
        Cs = Cs[1:]
        NLL = NLL[1:]
    # loop through CLs to determine limits
    NLL_cuts = []
    LLs = []
    ULs = []
    Cs_best = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # get rid of nans
        NLL[np.isnan(NLL)] = 1000.
        # find best value for FT0
        imin = np.argmin(NLL)
        C_best = Cs[imin]
        Cs_best.append(C_best)
        # FIXME! do something more clever than this?
        mask_excluded = NLL > NLL_cut
        LL = np.min(Cs[~mask_excluded])
        UL = np.max(Cs[~mask_excluded])
        LLs.append(LL)
        ULs.append(UL)
    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    LLs = np.array(LLs)
    ULs = np.array(ULs)
    Cs_best = np.array(Cs_best)
    return Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best
