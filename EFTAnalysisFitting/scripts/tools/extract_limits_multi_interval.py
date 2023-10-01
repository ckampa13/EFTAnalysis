# import from this file to get limits from an output root file
import numpy as np
import uproot
from scipy.stats import norm

CL_1sigma = 1. - 2.*norm.cdf(-1, loc=0, scale=1)

def lin_interp_to_cutoff(x0, x1, y0, y1, cutoff):
    slope = (y1-y0) / (x1-x0)
    # y = slope * (x-x0) + y0
    # x = (y-y0)/slope + x0
    x = (cutoff - y0) / slope + x0
    return x

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

def get_lims(CL_list, Cs=None, NLL=None, root_file=None, WC='cW', extrapolate=True):
    # load from file, if FT0 & NLL not supplied
    if Cs is None:
        Cs, NLL = get_NLL(root_file, WC)
    # loop through CLs to determine limits
    NLL_cuts = []
    LLs = []
    ULs = []
    LLs_interp = []
    ULs_interp = []
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
        NLL_best = NLL[imin]
        # find interval(s)
        mask_excluded = NLL > NLL_cut
        # calculate locations of crossings from positive to negative and reverse
        mask_diff = np.diff(mask_excluded.astype(int))
        xing_inds_p_to_n = np.where(mask_diff < 0)[0]
        xing_inds_n_to_p = np.where(mask_diff > 0)[0]
        if len(xing_inds_p_to_n) == len(xing_inds_n_to_p):
            # check if both ends open
            if (not mask_excluded[0]) and (not mask_excluded[-1]):
                LL = np.concatenate([[Cs[0]], Cs[xing_inds_p_to_n + 1]])
                #UL = np.concatenate([[Cs[-1]], Cs[xing_inds_n_to_p]])
                UL = np.concatenate([Cs[xing_inds_n_to_p], [Cs[-1]]])
                # interpolate for LL
                iLL = []
                # extrapolate endpoints
                if extrapolate:
                    loop_inds = np.concatenate([[0], xing_inds_p_to_n])
                    to_add = None
                else:
                    loop_inds = xing_inds_p_to_n
                    to_add = [Cs[0]]
                if not to_add is None:
                    for i in to_add:
                        iLL.append(i)
                for ind in loop_inds:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                # interpolate for UL
                iUL = []
                if extrapolate:
                    loop_inds = np.concatenate([xing_inds_n_to_p, [-2]])
                    to_add = None
                else:
                    loop_inds = xing_inds_n_to_p
                    to_add = [Cs[-1]]
                for ind in loop_inds:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                if not to_add is None:
                    for i in to_add:
                        iUL.append(i)
                #LL_interp = np.concatenate([[Cs[0]], iLL])
                #UL_interp = np.concatenate([iUL, [Cs[-1]]])
                LL_interp = iLL
                UL_interp = iUL
            else:
                LL = Cs[xing_inds_p_to_n + 1]
                UL = Cs[xing_inds_n_to_p]
                # interpolate for LL
                iLL = []
                for ind in xing_inds_p_to_n:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                # interpolate for UL
                iUL = []
                for ind in xing_inds_n_to_p:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                #LL_interp = np.concatenate([[Cs[0]], iLL])
                #UL_interp = np.concatenate([iUL, [Cs[-1]]])
                LL_interp = iLL
                UL_interp = iUL
        # interval is open on the left
        elif len(xing_inds_p_to_n) < len(xing_inds_n_to_p):
            LL = np.concatenate([[Cs[0]], Cs[xing_inds_p_to_n + 1]])
            UL = Cs[xing_inds_n_to_p]
            # interpolate for LL
            iLL = []
            # extrapolate endpoints
            if extrapolate:
                loop_inds = np.concatenate([[0], xing_inds_p_to_n])
                to_add = None
            else:
                loop_inds = xing_inds_p_to_n
                to_add = [Cs[0]]
            if not to_add is None:
                for i in to_add:
                    iLL.append(i)
            # extrapolate endpoints
            for ind in loop_inds:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            # interpolate for UL
            iUL = []
            for ind in xing_inds_n_to_p:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            #LL_interp = np.concatenate([[Cs[0]], iLL])
            #UL_interp = np.concatenate([iUL, [Cs[-1]]])
            LL_interp = iLL
            UL_interp = iUL
        # interval is open on the right
        else:
            LL = Cs[xing_inds_p_to_n + 1]
            UL = np.concatenate([[Cs[-1]], Cs[xing_inds_n_to_p]])
            # interpolate for LL
            iLL = []
            # extrapolate endpoints
            for ind in xing_inds_p_to_n:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            # interpolate for UL
            iUL = []
            if extrapolate:
                loop_inds = np.concatenate([xing_inds_n_to_p, [-2]])
                to_add = None
            else:
                loop_inds = xing_inds_n_to_p
                to_add = [Cs[-1]]
            for ind in loop_inds:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            if not to_add is None:
                for i in to_add:
                    iUL.append(i)
            #LL_interp = np.concatenate([[Cs[0]], iLL])
            #UL_interp = np.concatenate([iUL, [Cs[-1]]])
            LL_interp = iLL
            UL_interp = iUL

        LLs.append(LL)
        ULs.append(UL)
        LLs_interp.append(np.array(LL_interp))
        ULs_interp.append(np.array(UL_interp))

    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    # LLs = np.array(LLs)
    # ULs = np.array(ULs)
    Cs_best = np.array(Cs_best)
    #return Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best
    return Cs, NLL, CL_list, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best

def get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=None, WC='cW', extrapolate=True):
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
    LLs_interp = []
    ULs_interp = []
    Cs_best = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # get rid of nans
        NLL[np.isnan(NLL)] = 1000.
        # find best value for FT0
        imin = np.argmin(NLL)
        #C_best = Cs[imin]
        Cs_best.append(C_best)
        # find interval(s)
        mask_excluded = NLL > NLL_cut
        # calculate locations of crossings from positive to negative and reverse
        mask_diff = np.diff(mask_excluded.astype(int))
        xing_inds_p_to_n = np.where(mask_diff < 0)[0]
        xing_inds_n_to_p = np.where(mask_diff > 0)[0]
        if len(xing_inds_p_to_n) == len(xing_inds_n_to_p):
            # check if both ends open
            if (not mask_excluded[0]) and (not mask_excluded[-1]):
                LL = np.concatenate([[Cs[0]], Cs[xing_inds_p_to_n + 1]])
                #UL = np.concatenate([[Cs[-1]], Cs[xing_inds_n_to_p]])
                UL = np.concatenate([Cs[xing_inds_n_to_p], [Cs[-1]]])
                # interpolate for LL
                iLL = []
                # extrapolate endpoints
                if extrapolate:
                    loop_inds = np.concatenate([[0], xing_inds_p_to_n])
                    to_add = None
                else:
                    loop_inds = xing_inds_p_to_n
                    to_add = [Cs[0]]
                if not to_add is None:
                    for i in to_add:
                        iLL.append(i)
                for ind in loop_inds:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                # interpolate for UL
                iUL = []
                if extrapolate:
                    loop_inds = np.concatenate([xing_inds_n_to_p, [-2]])
                    to_add = None
                else:
                    loop_inds = xing_inds_n_to_p
                    to_add = [Cs[-1]]
                for ind in loop_inds:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                if not to_add is None:
                    for i in to_add:
                        iUL.append(i)
                #LL_interp = np.concatenate([[Cs[0]], iLL])
                #UL_interp = np.concatenate([iUL, [Cs[-1]]])
                LL_interp = iLL
                UL_interp = iUL
            else:
                LL = Cs[xing_inds_p_to_n + 1]
                UL = Cs[xing_inds_n_to_p]
                # interpolate for LL
                iLL = []
                for ind in xing_inds_p_to_n:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                # interpolate for UL
                iUL = []
                for ind in xing_inds_n_to_p:
                    x0 = Cs[ind]
                    x1 = Cs[ind+1]
                    y0 = NLL[ind]
                    y1 = NLL[ind+1]
                    iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
                #LL_interp = np.concatenate([[Cs[0]], iLL])
                #UL_interp = np.concatenate([iUL, [Cs[-1]]])
                LL_interp = iLL
                UL_interp = iUL
        # interval is open on the left
        elif len(xing_inds_p_to_n) < len(xing_inds_n_to_p):
            LL = np.concatenate([[Cs[0]], Cs[xing_inds_p_to_n + 1]])
            UL = Cs[xing_inds_n_to_p]
            # interpolate for LL
            iLL = []
            # extrapolate endpoints
            if extrapolate:
                loop_inds = np.concatenate([[0], xing_inds_p_to_n])
                to_add = None
            else:
                loop_inds = xing_inds_p_to_n
                to_add = [Cs[0]]
            if not to_add is None:
                for i in to_add:
                    iLL.append(i)
            # extrapolate endpoints
            for ind in loop_inds:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            # interpolate for UL
            iUL = []
            for ind in xing_inds_n_to_p:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            #LL_interp = np.concatenate([[Cs[0]], iLL])
            #UL_interp = np.concatenate([iUL, [Cs[-1]]])
            LL_interp = iLL
            UL_interp = iUL
        # interval is open on the right
        else:
            LL = Cs[xing_inds_p_to_n + 1]
            UL = np.concatenate([[Cs[-1]], Cs[xing_inds_n_to_p]])
            # interpolate for LL
            iLL = []
            # extrapolate endpoints
            for ind in xing_inds_p_to_n:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iLL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            # interpolate for UL
            iUL = []
            if extrapolate:
                loop_inds = np.concatenate([xing_inds_n_to_p, [-2]])
                to_add = None
            else:
                loop_inds = xing_inds_n_to_p
                to_add = [Cs[-1]]
            for ind in loop_inds:
                x0 = Cs[ind]
                x1 = Cs[ind+1]
                y0 = NLL[ind]
                y1 = NLL[ind+1]
                iUL.append(lin_interp_to_cutoff(x0, x1, y0, y1, NLL_cut))
            if not to_add is None:
                for i in to_add:
                    iUL.append(i)
            #LL_interp = np.concatenate([[Cs[0]], iLL])
            #UL_interp = np.concatenate([iUL, [Cs[-1]]])
            LL_interp = iLL
            UL_interp = iUL

        LLs.append(LL)
        ULs.append(UL)
        LLs_interp.append(np.array(LL_interp))
        ULs_interp.append(np.array(UL_interp))

    CL_list = np.array(CL_list)
    NLL_cuts = np.array(NLL_cuts)
    # LLs = np.array(LLs)
    # ULs = np.array(ULs)
    Cs_best = np.array(Cs_best)
    #return Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best
    return Cs, NLL, CL_list, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best
