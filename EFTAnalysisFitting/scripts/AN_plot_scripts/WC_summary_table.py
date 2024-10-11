import os
import numpy as np
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
#from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs
from tools.extract_limits_multi_interval import *
from MISC_CONFIGS import dim6_ops, WC_pretty_print_dict_AN
from tools.plotting_AN import numerical_formatter

WC_pretty_print_dict = WC_pretty_print_dict_AN

def print_summary_table_lim_sorted(ddir, dim, dim_dict, CL=0.95):
    CL_list = [CL]
    WCs = dim_dict[dim]
    # loop and get limits
    ULs = []
    LLs = []
    L_widths = []
    ULs_s = []
    LLs_s = []
    s_ULs = []
    s_LLs = []
    s_ULs_s = []
    s_LLs_s = []
    L_widths_s = []
    pdiffs = []
    s_pdiffs = []
    #pdiffs_s = []
    s_prints = []
    for WC in WCs:
        #print(WC)
        fname = ddir+f'full_analysis/higgsCombine_Asimov.all_combined.{WC}_1D.vCONFIG_VERSIONS.syst.MultiDimFit.mH120.root'
        fname_s = ddir+f'full_analysis/higgsCombine_Asimov.all_combined.{WC}_1D.vCONFIG_VERSIONS.nosyst.MultiDimFit.mH120.root'
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname, WC=WC, extrapolate=True)
        Cs, NLL, CL_list_, NLL_cuts, LLs_, ULs_, LLs_interp, ULs_interp, C_best, NLL_best = _
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname_s, WC=WC, extrapolate=True)
        Cs_s, NLL_s, CL_list_s, NLL_cuts_s, LLs_s_, ULs_s_, LLs_interp_s, ULs_interp_s, C_best_s, NLL_best_s = _
        # print
        LL_ = np.min(LLs_interp[0])
        LL_s = np.min(LLs_interp_s[0])
        UL_ = np.max(ULs_interp[0])
        UL_s = np.max(ULs_interp_s[0])
        # debug
        #print(f'UL_={UL_}\nLL_={LL_}\nUL_s={UL_s}\nLL_s={LL_s}')
        v_list = [LL_, UL_, LL_s, UL_s]
        s_list = []
        for v_ in v_list:
            s_list.append(f'{numerical_formatter(v_)}')
#             if abs(v_) < 0.1:
#                 s_list.append(f'{v_:0.3f}')
#             elif abs(v_) < 2.0:
#                 #s_list.append(f'{v_:0.2f}')
#                 s_list.append(f'{v_:0.3f}')
#             elif abs(v_) < 10.:
#                 s_list.append(f'{v_:0.1f}')
#             else:
#                 i_ = int(round(v_))
#                 s_list.append(f'{i_}')
        WC_ = f'{WC}:'
        lim = f'[{s_list[0]}, {s_list[1]}]'
        lim_s = f'[{s_list[2]}, {s_list[3]}]'
        L_width = UL_ - LL_
        L_width_s = UL_s - LL_s
        L_widths.append(L_width)
        L_widths_s.append(L_width_s)
        # calculate percentage difference in limit width
        pdiff = (L_width_s - L_width) / L_width
        pdiffs.append(pdiff)
        s_pdiff = f'{numerical_formatter(pdiff*100)}'
        s_pdiffs.append(s_pdiff)
        ULs.append(UL_)
        LLs.append(LL_)
        ULs_s.append(UL_s)
        LLs_s.append(LL_s)
        s_ULs.append(numerical_formatter(UL_))
        s_LLs.append(numerical_formatter(LL_))
        s_ULs_s.append(numerical_formatter(UL_s))
        s_LLs_s.append(numerical_formatter(LL_s))
        s_prints.append(f'{WC_:>6} {lim:>20} (syst), {lim_s:>20} (stat only)')
    L_widths = np.array(L_widths)
    L_widths_s = np.array(L_widths_s)
    pdiffs = np.array(pdiffs)
    s_pdiffs = np.array(s_pdiffs)
    # debug
    #print(f'ULs={ULs}\nLLs={LLs}\nULs_s={ULs_s}\nLLs_s={LLs_s}')
    #
    ULs = np.array(ULs)
    LLs = np.array(LLs)
    ULs_s = np.array(ULs_s)
    LLs_s = np.array(LLs_s)
    s_ULs = np.array(s_ULs)
    s_LLs = np.array(s_LLs)
    s_ULs_s = np.array(s_ULs_s)
    s_LLs_s = np.array(s_LLs_s)
    s_prints = np.array(s_prints)
    s_prints_s = np.array(s_prints)
    inds = np.arange(len(WCs))
    inds_sort = inds[np.argsort(L_widths_s)]
    WCs_sorted = np.array(WCs)[inds_sort]
    pdiffs = pdiffs[inds_sort]
    s_pdiffs = s_pdiffs[inds_sort]
    for counter, i in enumerate(inds_sort):
        print(s_prints[i])
        # nicer spacing for plot matrix
        if (counter+1) % 6 == 0:
            print()
    return s_prints[inds_sort], WCs_sorted, s_pdiffs, s_ULs[inds_sort], s_LLs[inds_sort], s_ULs_s[inds_sort], s_LLs_s[inds_sort]

def make_summary_table(WCs, LLs, ULs, dim='dim6', tex_file=None):
    # Construct the LaTeX table as a string
    table = r"\begin{table}[hbtp!]" + "\n"
    table += r"\centering" + "\n"
    table += r"\begin{tabular}{l|c}" + "\n"
    table += r"\hline" + "\n"
    #table += r"Wilson coefficient & Impact on 95\% CL Limits \\ [\% Change in Interval Width] \\" + "\n"
    if dim == 'dim6':
        table += r"Wilson coefficient & \multicolumn{1}{|p{5cm}}{\centering Expected 95\% CL Limits \\ $[$TeV$^{-2}]$} \\" + "\n"
        wc_suff = r'/\Lambda^{2}$'
    else:
        table += r"Wilson coefficient & \multicolumn{1}{|p{5cm}}{\centering Expected 95\% CL Limits \\ $[$TeV$^{-4}]$} \\" + "\n"
        wc_suff = r'/\Lambda^{4}$'
    table += r"\hline" + "\n"

    # Add the rows to the table
    for WC, val_L, val_U in zip(WCs, LLs, ULs):
        WC_p = WC_pretty_print_dict[WC].rstrip('$') + wc_suff
        table += f"{WC_p} & $[{val_L}, {val_U}]$ \\\\" + "\n"

    table += r"\hline" + "\n"
    table += r"\end{tabular}" + "\n"
    if dim == 'dim6':
        table += r"\caption{A summary of the expected 95\% CL limits on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing limit interval width.}" + "\n"
    else:
        table += r"\caption{A summary of the expected 95\% CL limits on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing limit interval width.}" + "\n"
    table += r"\label{tab:limit_summary_"+f"{dim}"+"}" + "\n"
    table += r"\end{table}" + "\n"

    print(table)

    if not tex_file is None:
        with open(tex_file, 'w') as f:
            f.write(table)
    return table


if __name__=='__main__':
    dim_dict = {'dim6': dim6_WCs, 'dim8': dim8_WCs,
                #'cW_test': ['cW'],
                #'dim8_partial': ['FS0', 'FS1', 'FS2', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4'],
               }
    ddir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'output')), '')
    plotdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'AN_plots', 'tables')), '')
    # with syst
    results_dict = {}
    print('Limits with systematics...')
    for dim in ['dim6', 'dim8']:
    #for dim in ['cW_test']:
    # for dim in ['dim6', 'dim8_partial']:
        print(f'{dim} Current Limit Ranking (full analysis):')
        s_prints, WCs_sorted, pdiffs, s_ULs, s_LLs, s_ULs_s, s_LLs_s = print_summary_table_lim_sorted(ddir, dim, dim_dict)
        results_dict[dim] = {'s_prints': s_prints, 'WCs_sorted': WCs_sorted, 'pdiffs': pdiffs,
                             's_ULs': s_ULs, 's_LLs': s_LLs, 's_ULs_s': s_ULs_s, 's_LLs_s': s_LLs_s}
        print('\n')
    #print(results_dict)
    # make tables, with systematics
    for dim in ['dim6', 'dim8']:
        make_summary_table(results_dict[dim]['WCs_sorted'], results_dict[dim]['s_LLs'], results_dict[dim]['s_ULs'], dim=dim, tex_file=plotdir+f'limit_summary_{dim}.tex')
