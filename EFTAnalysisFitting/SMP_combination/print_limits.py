import sys
sys.path.append('../scripts/tools/')
from extract_limits_multi_interval import get_lims

if __name__=='__main__':
    fname = 'higgsCombine_VVV_nogamma_cW_1D.MultiDimFit.mH120.root'
    WC = 'cW'
    Cs, NLL, CL_list, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best = get_lims(CL_list=[0.95], Cs=None, NLL=None, root_file=fname, WC=WC, extrapolate=True)
    # print the limits
    Cs_ = [round(C, 2) for C in Cs]
    NLL_ = [round(N, 2) for N in NLL]
    print('\n\nScanning %s:' % WC)
    print('cW = %s' % Cs_)
    print('NLL = %s' % NLL_)
    print('95%% CL Limits: [%0.3f, %0.3f]' % (LLs_interp[0][0], ULs_interp[0][0]))
    print('\n\nTEST COMPLETE!')
