import os
import argparse
import numpy as np
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
#from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, dim8_WCs_sort_AN
from tools.extract_limits_multi_interval import *
from MISC_CONFIGS import dim6_ops, WC_pretty_print_dict_AN, WC_pretty_print_dict_paper
from tools.plotting_AN import numerical_formatter, get_ndec, match_ndec, check_all_zero

#WC_pretty_print_dict = WC_pretty_print_dict_AN
WC_pretty_print_dict = WC_pretty_print_dict_paper # aliases

def print_summary_table_lim_sorted(ddir, dim, dim_dict, CL_list=[0.95, CL_1sigma], order_sens=True):
    ##CL_list = [CL]
    WCs = dim_dict[dim]
    # loop and get limits
    ULs_a = []
    LLs_a = []
    L_widths_a = []
    WC_bests_a = []
    s_WC_bests_a = []
    ULs_d = []
    LLs_d = []
    s_ULs_a = []
    s_LLs_a = []
    s_ULs_d = []
    s_LLs_d = []
    L_widths_d = []
    WC_bests_d = []
    s_WC_bests_d = []
    pdiffs = []
    s_pdiffs = []
    #pdiffs_s = []
    s_prints = []
    meas_dicts = []
    for WC in WCs:
        #print(WC)
        fname_a = ddir+f'full_analysis/higgsCombine_Asimov.all_combined.{WC}_1D.vCONFIG_VERSIONS.syst.MultiDimFit.mH120.root'
        fname_d = ddir+f'full_analysis/higgsCombine_Data.all_combined.{WC}_1D.vCONFIG_VERSIONS.syst.MultiDimFit.mH120.root'
        #_ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname_a, WC=WC, extrapolate=True)
        _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_a, WC=WC, extrapolate=True)
        # _ = get_lims_quad_interp(CL_list, Cs=None, NLL=None, root_file=fname_a, WC=WC, extrapolate=True, kind='linear')
        Cs_a, NLL_a, CL_list_a, NLL_cuts_a, LLs_a_, ULs_a_, LLs_interp_a, ULs_interp_a, C_best_a, NLL_best_a = _
        #_ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True)
        # special cases in data where combine best fit is not at NLL min
        #if WC in ['cHl3', 'cll1', 'cHbox', 'cHDD']:
        #    _ = get_lims_quad_interp(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True, kind='linear')
        #else:
        #    _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True)
        #_ = get_lims_quad_interp(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True, kind='linear')
        _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True)
        Cs_d, NLL_d, CL_list_d, NLL_cuts_d, LLs_d_, ULs_d_, LLs_interp_d, ULs_interp_d, C_best_d, NLL_best_d = _
        # separately get point estimate(s) and +- values (1 sigma)
        C_bests_1s_d, NLL_bests_1s_d, pluss_1s_d, minuss_1s_d, bounds_1s_d = get_point_estimate_pm_1sigma(Cs_d, NLL_d, LLs_interp_d[1], ULs_interp_d[1], C_best_d, use_best=True, dC=0.001, kind='linear')
        C_bests_1s_a, NLL_bests_1s_a, pluss_1s_a, minuss_1s_a, bounds_1s_a = get_point_estimate_pm_1sigma(Cs_a, NLL_a, LLs_interp_a[1], ULs_interp_a[1], C_best_a, use_best=True, dC=0.001, kind='linear')
        # dictionary to pass on
        meas_dict = {
            'Data': {
                'C_bests': C_bests_1s_d, 'NLL_bests': NLL_bests_1s_d,
                'pluss': pluss_1s_d, 'minuss': minuss_1s_d, 'bounds': bounds_1s_d,
            },
            'Asimov': {
                'C_bests': C_bests_1s_a, 'NLL_bests': NLL_bests_1s_a,
                'pluss': pluss_1s_a, 'minuss': minuss_1s_a, 'bounds': bounds_1s_a,
            },
        }
        #meas_dicts.append(meas_dict)
        # best values
        WC_bests_a.append(C_best_a)
        WC_bests_d.append(C_best_d)
        s_best_a = numerical_formatter(C_best_a)
        s_WC_bests_a.append(s_best_a)
        s_best_d = numerical_formatter(C_best_d)
        s_WC_bests_d.append(s_best_d)
        # print
        # need to handle case of multiple intervals
        # LL_a = np.min(LLs_interp_a[0])
        # LL_d = np.min(LLs_interp_d[0])
        # UL_a = np.max(ULs_interp_a[0])
        # UL_d = np.max(ULs_interp_d[0])
        LL_a = LLs_interp_a[0]
        LL_d = LLs_interp_d[0]
        UL_a = ULs_interp_a[0]
        UL_d = ULs_interp_d[0]
        # also want range
        LL_a_r = np.min(LLs_interp_a[0])
        LL_d_r = np.min(LLs_interp_d[0])
        UL_a_r = np.max(ULs_interp_a[0])
        UL_d_r = np.max(ULs_interp_d[0])
        # debug
        #print(f'UL_={UL_}\nLL_={LL_}\nUL_s={UL_s}\nLL_s={LL_s}')
        v_list = [LL_a, UL_a, LL_d, UL_d]
        s_list = []
        for v_ in v_list:
            s_ = []
            for v in v_:
                s_.append(numerical_formatter(v))
            s_list.append(s_)
            #s_list.append(f'{numerical_formatter(v_)}')
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
        #lim_a = f'[{s_list[0]}, {s_list[1]}]'
        #lim_d = f'[{s_list[2]}, {s_list[3]}]'
        lim_a_ = []
        for s0, s1 in zip(s_list[0], s_list[1]):
            lim_a_.append(f'[{s0}, {s1}]')
        lim_d_ = []
        for s0, s1 in zip(s_list[2], s_list[3]):
            lim_d_.append(f'[{s0}, {s1}]')
        lim_a = 'v'.join(lim_a_)
        lim_d = 'v'.join(lim_d_)
        L_width_a = UL_a_r - LL_a_r
        L_width_d = UL_d_r - LL_d_r
        L_widths_a.append(L_width_a)
        L_widths_d.append(L_width_d)
        # calculate percentage difference in limit width
        pdiff = (L_width_d - L_width_a) / L_width_a
        pdiffs.append(pdiff)
        s_pdiff = f'{numerical_formatter(pdiff*100)}'
        s_pdiffs.append(s_pdiff)
        ULs_a.append(UL_a)
        LLs_a.append(LL_a)
        ULs_d.append(UL_d)
        LLs_d.append(LL_d)
        # s_ULs_a.append(numerical_formatter(UL_a))
        # s_LLs_a.append(numerical_formatter(LL_a))
        # s_ULs_d.append(numerical_formatter(UL_d))
        # s_LLs_d.append(numerical_formatter(LL_d))
        s_ULs_a.append([numerical_formatter(UL_) for UL_ in UL_a])
        s_LLs_a.append([numerical_formatter(LL_) for LL_ in LL_a])
        s_ULs_d.append([numerical_formatter(UL_) for UL_ in UL_d])
        s_LLs_d.append([numerical_formatter(LL_) for LL_ in LL_d])
        #s_prints.append(f'{WC_:>6} ={s_best_a:>10}, {lim_a:>20} (asimov); ={s_best_d:>10}, {lim_d:>20} (data)')
        s_prints.append(f'{WC_:>6} {lim_a:>20} (asimov); {lim_d:>20} (data)')
        # add point estimates
        s_meas = []
        s_meas_tex = []
        md = meas_dict['Asimov']
        for Cb, p, m in zip(md['C_bests'], md['pluss'], md['minuss']):
            #Cb_ = numerical_formatter(Cb)
            #p_, _ = match_ndec(p, Cb_)
            #m_, _ = match_ndec(m, Cb_)
            m_ = numerical_formatter(m)
            p_ = numerical_formatter(p)
            num_m = get_ndec(m_)
            num_p = get_ndec(p_)
            if num_m < num_p:
                Cb_, _ = match_ndec(Cb, m_)
            else:
                Cb_, _ = match_ndec(Cb, p_)
            # clean trailing negative
            if check_all_zero(Cb_):
                Cb_ = Cb_.lstrip('-')
            s_meas.append(f'{Cb_}+{p_}-{m_}')
            s_meas_tex.append(f'${Cb_}^{{+{p_}}}_{{- {m_} }}$')
        meas_dict['Asimov']['tex_string_list'] = s_meas_tex
        ss_meas_a = ' or '.join(s_meas)
        s_meas = []
        s_meas_tex = []
        md = meas_dict['Data']
        for Cb, p, m in zip(md['C_bests'], md['pluss'], md['minuss']):
            #Cb_ = numerical_formatter(Cb)
            #p_, _ = match_ndec(p, Cb_)
            #m_, _ = match_ndec(m, Cb_)
            m_ = numerical_formatter(m)
            p_ = numerical_formatter(p)
            num_m = get_ndec(m_)
            num_p = get_ndec(p_)
            if num_m < num_p:
                Cb_, _ = match_ndec(Cb, m_)
            else:
                Cb_, _ = match_ndec(Cb, p_)
            # clean trailing negative
            if check_all_zero(Cb_):
                Cb_ = Cb_.lstrip('-')
            s_meas.append(f'{Cb_}+{p_}-{m_}')
            s_meas_tex.append(f'${Cb_}^{{+{p_}}}_{{- {m_} }}$')
        meas_dict['Data']['tex_string_list'] = s_meas_tex
        ss_meas_d = ' or '.join(s_meas)
        s_prints[-1]+= f'\n{ss_meas_a} (asimov); {ss_meas_d} (data)\n'
        meas_dicts.append(meas_dict)
    L_widths_a = np.array(L_widths_a)
    L_widths_d = np.array(L_widths_d)
    pdiffs = np.array(pdiffs)
    s_pdiffs = np.array(s_pdiffs)
    # debug
    #print(f'ULs={ULs}\nLLs={LLs}\nULs_s={ULs_s}\nLLs_s={LLs_s}')
    #
    #ULs_a = np.array(ULs_a)
    #LLs_a = np.array(LLs_a)
    #ULs_d = np.array(ULs_d)
    #LLs_d = np.array(LLs_d)
    #s_ULs_a = np.array(s_ULs_a)
    #s_LLs_a = np.array(s_LLs_a)
    #s_ULs_d = np.array(s_ULs_d)
    #s_LLs_d = np.array(s_LLs_d)
    s_prints = np.array(s_prints)
    WC_bests_a = np.array(WC_bests_a)
    WC_bests_d = np.array(WC_bests_d)
    s_WC_bests_a = np.array(s_WC_bests_a)
    s_WC_bests_d = np.array(s_WC_bests_d)
    inds = np.arange(len(WCs))
    if order_sens:
        inds_sort = inds[np.argsort(L_widths_d)]
    else:
        inds_sort = inds
    WCs_sorted = np.array(WCs)[inds_sort]
    pdiffs = pdiffs[inds_sort]
    s_pdiffs = s_pdiffs[inds_sort]
    for counter, i in enumerate(inds_sort):
        print(s_prints[i])
        # nicer spacing for plot matrix
        if (counter+1) % 6 == 0:
            print()
    # reorder lists
    lscope = {'inds_sort': inds_sort, 'ULs_a': ULs_a, 'LLs_a': LLs_a, 'ULs_d': ULs_d, 'LLs_d': LLs_d, 's_ULs_a': s_ULs_a, 's_LLs_a': s_LLs_a, 's_ULs_d': s_ULs_d, 's_LLs_d': s_LLs_d, 'meas_dicts': meas_dicts}
    for l in ['ULs_a', 'LLs_a', 'ULs_d', 'LLs_d', 's_ULs_a', 's_LLs_a', 's_ULs_d', 's_LLs_d', 'meas_dicts']:
        exec(f'{l}_temp = [{l}[i] for i in inds_sort]', lscope)
        exec(f'{l} = {l}_temp', lscope)
    #return s_prints[inds_sort], WCs_sorted, s_pdiffs, s_ULs_a[inds_sort], s_LLs_a[inds_sort], s_ULs_d[inds_sort], s_LLs_d[inds_sort], s_WC_bests_a[inds_sort], s_WC_bests_d[inds_sort]
    return s_prints[inds_sort], WCs_sorted, s_pdiffs, lscope['s_ULs_a'], lscope['s_LLs_a'], lscope['s_ULs_d'], lscope['s_LLs_d'], s_WC_bests_a[inds_sort], s_WC_bests_d[inds_sort], lscope['meas_dicts']

# 2 column
# def make_summary_table(WCs, LLs_a, ULs_a , LLs_d, ULs_d, WCs_bests_a, WCs_bests_d, dim='dim6', order_sens=True, tex_file=None):
#     # Construct the LaTeX table as a string
#     table = r"\begin{table}[hbtp!]" + "\n"
#     table += r"\centering" + "\n"
#     table += r"\begin{tabular}{l|c|c}" + "\n"
#     table += r"\hline" + "\n"
#     #table += r"Wilson coefficient & Impact on 95\% CL Limits \\ [\% Change in Interval Width] \\" + "\n"
#     if dim == 'dim6':
#         table += r"Wilson coefficient & \multicolumn{1}{|p{5cm}}{\centering Observed (Expected) \\ 95\% CL Limits \\ $[$TeV$^{-2}]$} & \multicolumn{1}{|p{5cm}}{\centering Observed (Expected) \\ Point Estimate \\ $[$TeV$^{-2}]$} \\" + "\n"
#         wc_suff = r'/\Lambda^{2}$'
#     else:
#         table += r"Wilson coefficient & \multicolumn{1}{|p{5cm}}{\centering Observed (Expected) \\ 95\% CL Limits \\ $[$TeV$^{-4}]$} & \multicolumn{1}{|p{5cm}}{\centering Observed (Expected) \\ Point Estimate \\ $[$TeV$^{-4}]$} \\" + "\n"
#         wc_suff = r'/\Lambda^{4}$'
#     table += r"\hline" + "\n"

#     # Add the rows to the table
#     for WC, val_L_a, val_U_a, val_L_d, val_U_d, bf_a, bf_d in zip(WCs, LLs_a, ULs_a, LLs_d, ULs_d, WCs_bests_a, WCs_bests_d):
#         WC_p = WC_pretty_print_dict[WC].rstrip('$') + wc_suff
#         d_str = []
#         for L, U in zip(val_L_d, val_U_d):
#             d_str.append(f"$[{L}, {U}]$")
#         d_str = r" $\cup$ ".join(d_str)
#         a_str = []
#         for L, U in zip(val_L_a, val_U_a):
#             a_str.append(f"$[{L}, {U}]$")
#         a_str = r" $\cup$ ".join(a_str)
#         table += f"{WC_p} & {d_str} ({a_str}) & ${bf_d}$ (${bf_a}$) \\\\" + "\n"

#     table += r"\hline" + "\n"
#     table += r"\end{tabular}" + "\n"

#     if order_sens:
#         if dim == 'dim6':
#             table += r"\caption{A summary of the 95\% CL limits on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing limit interval width.}" + "\n"
#         else:
#             table += r"\caption{A summary of the 95\% CL limits on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing limit interval width.}" + "\n"
#         table += r"\label{tab:limit_summary_"+f"{dim}"+"}" + "\n"
#     else:
#         if dim == 'dim6':
#             table += r"\caption{A summary of the 95\% CL limits on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
#         else:
#             table += r"\caption{A summary of the 95\% CL limits on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
#         table += r"\label{tab:limit_summary_"+f"{dim}"+"_alt_order}" + "\n"
#     table += r"\end{table}" + "\n"

#     print(table)

#     if not tex_file is None:
#         with open(tex_file, 'w') as f:
#             f.write(table)
#     return table

# 4 column
def make_summary_table(WCs, LLs_a, ULs_a , LLs_d, ULs_d, WCs_bests_a, WCs_bests_d, meas_dicts, dim='dim6', order_sens=True, tex_file=None):
    # Construct the LaTeX table as a string
    table = r"\begin{table}[hbtp!]" + "\n"
    table += r"\centering" + "\n"
    # caption
    if order_sens:
        table += r"\label{tab:limit_summary_"+f"{dim}"+"}" + "\n"
        if dim == 'dim6':
            table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing bounds interval width.}" + "\n"
        else:
            table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing bounds interval width.}" + "\n"
    else:
        table += r"\label{tab:limit_summary_"+f"{dim}"+"_alt_order}" + "\n"
        if dim == 'dim6':
            table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
        else:
            table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
    #table += r"\end{table}" + "\n"
    table += r"\begin{tabular}{r|c|c|c}" + "\n"
    table += r"\hline" + "\n"
    #table += r"Wilson coefficient & Impact on 95\% CL Limits \\ [\% Change in Interval Width] \\" + "\n"
    if dim == 'dim6':
        #table += r"\multicolumn{1}{p{2cm}|}{\raggedleft Wilson \\ coefficient} & \multicolumn{1}{p{3.5cm}|}{\centering Observed \\ 95\% CL Limits \\ $[$TeV$^{-2}]$} & \multicolumn{1}{p{3.5cm}|}{\centering Expected \\ 95\% CL Limits \\ $[$TeV$^{-2}]$} & \multicolumn{1}{p{2cm}|}{\centering Observed \\ Point Estimate \\ $[$TeV$^{-2}]$} & \multicolumn{1}{p{2cm}}{\centering Expected \\ Point Estimate \\ $[$TeV$^{-2}]$} \\" + "\n"
        table += r"Wilson & \multicolumn{2}{p{7cm}|}{\centering 95\% CL Bounds $[$TeV$^{-2}]$} & \multicolumn{1}{p{4cm}}{\centering Measurement $[$TeV$^{-2}]$} \\" + "\n"
        table += r"coefficient & \multicolumn{1}{p{3.5cm}|}{\centering Observed} & Expected & Observed\\" + "\n"
        wc_suff = r'/\Lambda^{2}$'
    else:
        #table += r"\multicolumn{1}{p{2cm}|}{\raggedleft Wilson \\ coefficient} & \multicolumn{1}{p{3.5cm}|}{\centering Observed \\ 95\% CL Limits \\ $[$TeV$^{-4}]$} & \multicolumn{1}{p{3.5cm}|}{\centering Expected \\ 95\% CL Limits \\ $[$TeV$^{-4}]$} & \multicolumn{1}{p{2cm}|}{\centering Observed \\ Point Estimate \\ $[$TeV$^{-4}]$} & \multicolumn{1}{p{2cm}}{\centering Expected \\ Point Estimate \\ $[$TeV$^{-4}]$} \\" + "\n"
        table += r"Wilson & \multicolumn{2}{p{7cm}|}{\centering 95\% CL Bounds $[$TeV$^{-4}]$} & \multicolumn{1}{p{4cm}}{\centering Measurement $[$TeV$^{-4}]$} \\" + "\n"
        table += r"coefficient & \multicolumn{1}{p{3.5cm}|}{\centering Observed} & Expected & Observed\\" + "\n"
        wc_suff = r'/\Lambda^{4}$'
    table += r"\hline" + "\n"

    # Add the rows to the table
    #for WC, val_L_a, val_U_a, val_L_d, val_U_d, bf_a, bf_d in zip(WCs, LLs_a, ULs_a, LLs_d, ULs_d, WCs_bests_a, WCs_bests_d):
    for WC, val_L_a, val_U_a, val_L_d, val_U_d, meas_dict in zip(WCs, LLs_a, ULs_a, LLs_d, ULs_d, meas_dicts):
        #WC_p = WC_pretty_print_dict[WC].rstrip('$') + wc_suff
        WC_p = "$"+ WC_pretty_print_dict[WC] + wc_suff
        d_str = []
        for L, U in zip(val_L_d, val_U_d):
            d_str.append(f"$[{L}, {U}]$")
        d_str = r" $\cup$ ".join(d_str)
        a_str = []
        for L, U in zip(val_L_a, val_U_a):
            a_str.append(f"$[{L}, {U}]$")
        a_str = r" $\cup$ ".join(a_str)
        meas_str = ' or '.join(meas_dict['Data']['tex_string_list'])
        #table += f"{WC_p} & {d_str} ({a_str}) & ${bf_d}$ (${bf_a}$) \\\\" + "\n"
        #table += f"{WC_p} & {d_str} & {a_str} & ${bf_d}$ & ${bf_a}$ \\\\" + "\n"
        table += f"{WC_p} & {d_str} & {a_str} & {meas_str} \\\\" + "\n"

    table += r"\hline" + "\n"
    table += r"\end{tabular}" + "\n"

    # if order_sens:
    #     if dim == 'dim6':
    #         table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing bounds interval width.}" + "\n"
    #     else:
    #         table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time. The Wilson coefficients are ordered by increasing bounds interval width.}" + "\n"
    #     table += r"\label{tab:limit_summary_"+f"{dim}"+"}" + "\n"
    # else:
    #     if dim == 'dim6':
    #         table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-6 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
    #     else:
    #         table += r"\caption{A summary of the 95\% CL bounds and measurements on the dimension-8 Wilson coefficients, when considering a single non-zero Wilson coefficient at a time.}" + "\n"
    #     table += r"\label{tab:limit_summary_"+f"{dim}"+"_alt_order}" + "\n"
    table += r"\end{table}" + "\n"

    print(table)

    if not tex_file is None:
        with open(tex_file, 'w') as f:
            f.write(table)
    return table



if __name__=='__main__':
    Unblind=True
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--Dimension',
                        help='Which dimension? ["all" (default), "dim6", "dim8"]')
    parser.add_argument('-o', '--OrderBySens',
                        help='Order by sensitivity? ["y" (default), "n" -- dim8 only so far]')
    args = parser.parse_args()
    if args.Dimension is None:
        dims = 'all'
    else:
        dims = args.Dimension
    if dims == 'all':
        dims_list = ['dim6', 'dim8']
    else:
        dims_list = [dims]
    if args.OrderBySens is None:
        order_sens = True
    else:
        order_sens = args.OrderBySens == 'y'

    dim_dict = {'dim6': dim6_WCs, 'dim8': dim8_WCs_sort_AN,
                #'cW_test': ['cW'],
                #'dim8_partial': ['FS0', 'FS1', 'FS2', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4'],
               }
    if Unblind:
        ddir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output')), '')
        plotdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'AN_plots', 'tables')), '')
    else:
        ddir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'output')), '')
        plotdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'AN_plots', 'tables')), '')
    # with syst
    results_dict = {}
    print('Limits with systematics...')
    for dim in dims_list:
    #for dim in ['dim6', 'dim8']:
    #for dim in ['cW_test']:
    # for dim in ['dim6', 'dim8_partial']:
        print(f'{dim} Current Limit Ranking (full analysis):')
        _ = print_summary_table_lim_sorted(ddir, dim, dim_dict, order_sens=order_sens)
        s_prints, WCs_sorted, pdiffs, s_ULs_a, s_LLs_a, s_ULs_d, s_LLs_d, s_WC_bests_a, s_WC_bests_d, meas_dicts = _
        results_dict[dim] = {'s_prints': s_prints, 'WCs_sorted': WCs_sorted, 'pdiffs': pdiffs,
                             's_ULs_a': s_ULs_a, 's_LLs_a': s_LLs_a, 's_ULs_d': s_ULs_d, 's_LLs_d': s_LLs_d,
                             's_WC_bests_a': s_WC_bests_a, 's_WC_bests_d': s_WC_bests_d,
                             'meas_dicts': meas_dicts}
        print('\n')

    #print(results_dict)
    # make tables, with systematics
    for dim in dims_list:
    #for dim in ['dim6', 'dim8']:
        if order_sens:
            tex_file = plotdir+f'limit_summary_{dim}.tex'
        else:
            tex_file = plotdir+f'limit_summary_{dim}_alt_order.tex'
        make_summary_table(results_dict[dim]['WCs_sorted'],
                           results_dict[dim]['s_LLs_a'], results_dict[dim]['s_ULs_a'],
                           results_dict[dim]['s_LLs_d'], results_dict[dim]['s_ULs_d'],
                           results_dict[dim]['s_WC_bests_a'], results_dict[dim]['s_WC_bests_d'],
                           results_dict[dim]['meas_dicts'],
                           dim=dim, order_sens=order_sens,
                           tex_file=tex_file)
