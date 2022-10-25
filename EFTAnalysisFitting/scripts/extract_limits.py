# import from this file to get limits from an output root file
import numpy as np
import uproot
from scipy.stats import norm

CL_1sigma = 1. - 2.*norm.cdf(-1, loc=0, scale=1)

def get_NLL(root_file):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array()[1:].tolist())
    FT0 = np.array(file_['limit']['k_cG'].array()[1:].tolist())

    return FT0, NLL

def get_NLL_full(root_file):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array().tolist())
    FT0 = np.array(file_['limit']['k_cG'].array().tolist())

    return FT0, NLL

def get_lims(CL_list, FT0=None, NLL=None, root_file=None):
    # load from file, if FT0 & NLL not supplied
    if FT0 is None:
        FT0, NLL = get_NLL(root_file)
    # loop through CLs to determine limits
    NLL_cuts = []
    LLs = []
    ULs = []
    FT0s_best = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # get rid of nans
        NLL[np.isnan(NLL)] = 1000.
        # find best value for FT0
        imin = np.argmin(NLL)
        FT0_best = FT0[imin]
        FT0s_best.append(FT0_best)
        # FIXME! do something more clever than this?
        mask_excluded = NLL > NLL_cut
        LL = np.min(FT0[~mask_excluded])
        UL = np.max(FT0[~mask_excluded])
        LLs.append(LL)
        ULs.append(UL)
    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    LLs = np.array(LLs)
    ULs = np.array(ULs)
    FT0s_best = np.array(FT0s_best)
    return FT0, NLL, CL_list, NLL_cuts, LLs, ULs

def get_lims_w_best(CL_list, FT0=None, NLL=None, root_file=None):
    # load from file, if FT0 & NLL not supplied
    if FT0 is None:
        FT0, NLL = get_NLL_full(root_file)
        FT0_best = FT0[0]
        NLL_best = NLL[0]
        FT0 = FT0[1:]
        NLL = NLL[1:]
    # loop through CLs to determine limits
    NLL_cuts = []
    LLs = []
    ULs = []
    FT0s_best = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # get rid of nans
        NLL[np.isnan(NLL)] = 1000.
        # find best value for FT0
        imin = np.argmin(NLL)
        FT0_best = FT0[imin]
        FT0s_best.append(FT0_best)
        # FIXME! do something more clever than this?
        mask_excluded = NLL > NLL_cut
        LL = np.min(FT0[~mask_excluded])
        UL = np.max(FT0[~mask_excluded])
        LLs.append(LL)
        ULs.append(UL)
    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    LLs = np.array(LLs)
    ULs = np.array(ULs)
    FT0s_best = np.array(FT0s_best)
    return FT0, NLL, CL_list, NLL_cuts, LLs, ULs, FT0_best, NLL_best
