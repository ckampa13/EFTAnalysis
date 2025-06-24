# import from this file to get limits from an output root file
import numpy as np
import uproot
from scipy.stats import norm
from scipy.interpolate import interp1d

CL_1sigma = 1. - 2.*norm.cdf(-1, loc=0, scale=1)

def lin_interp_to_cutoff(x0, x1, y0, y1, cutoff):
    slope = (y1-y0) / (x1-x0)
    # y = slope * (x-x0) + y0
    # x = (y-y0)/slope + x0
    x = (cutoff - y0) / slope + x0
    return x

def get_NLL(root_file, WC='cW', update_min=True):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array()[1:].tolist())
    if update_min:
        NLL = NLL - np.min(NLL)
    if WC == 'sm':
        x_col = 'r'
    else:
        x_col = 'k_'+WC
    Cs = np.array(file_['limit'][x_col].array()[1:].tolist())

    return Cs, NLL

def get_NLL_full(root_file, WC='cW', update_min=True):
    file_ = uproot.open(root_file)
    NLL = np.array(file_['limit']['deltaNLL'].array().tolist())
    if update_min:
        NLL = NLL - np.min(NLL)
    if WC == 'sm':
        x_col = 'r'
    else:
        x_col = 'k_'+WC
    Cs = np.array(file_['limit'][x_col].array().tolist())

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

def get_lims_quad_interp(CL_list, Cs=None, NLL=None, root_file=None, WC='cW', extrapolate=True, dC=0.0001, ndec=4, kind='quadratic'):
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
        # set up interpolation function
        interp_func = interp1d(Cs, NLL, kind=kind)
        Cmin = np.round(Cs[0], decimals=ndec) + dC
        Cmax = np.round(Cs[-1], decimals=ndec) - dC
        Cs_fine = np.arange(Cmin, Cmax+dC, dC)
        NLL_fine = interp_func(Cs_fine)
        imin = np.argmin(NLL_fine)
        C_best = Cs_fine[imin]
        Cs_best.append(C_best)
        NLL_best = NLL_fine[imin]
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

def get_point_estimate_pm_1sigma(Cs, NLL, LLs_interp_1sigma, ULs_interp_1sigma, C_best_combine, use_best=True, dC=0.0001, kind='quadratic'):
    # assumes LLs_interp_1sigma and ULs_interp_1sigma were grabbed from LLs_interp and ULs_interp
    # generated with CL_1sigma
    bounds = []
    C_bests = []
    NLL_bests = []
    pluss = []
    minuss = []
    for LL, UL in zip(LLs_interp_1sigma, ULs_interp_1sigma):
        # find point estimate only within this range
        # set up interpolation function
        interp_func = interp1d(Cs, NLL, kind=kind, fill_value='extrapolate')
        LL_ = np.round(LL) - 1
        UL_ = np.round(UL) + 1
        Cs_fine = np.arange(LL_, UL_, dC)
        NLL_fine = interp_func(Cs_fine)
        imin = np.argmin(NLL_fine)
        C_best = Cs_fine[imin]
        if use_best:
            if abs(C_best - C_best_combine) < 1.:
                C_best = C_best_combine
        C_bests.append(C_best)
        NLL_best = NLL_fine[imin]
        NLL_bests.append(NLL_best)
        plus = UL - C_best
        minus = C_best - LL
        pluss.append(plus)
        minuss.append(minus)
        bounds.append([LL, UL])
    return C_bests, NLL_bests, pluss, minuss, bounds

