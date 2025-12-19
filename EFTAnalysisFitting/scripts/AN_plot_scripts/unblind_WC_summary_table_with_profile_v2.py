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
    results_dict = {}
    for freeze in [True, False]:
        if freeze:
            freeze_str = 'Freeze'
        else:
            freeze_str = 'Profile'
        print(f'{freeze_str}:')
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
            if freeze:
                fname_a = ddir+f'full_analysis/higgsCombine_Asimov.all_combined.{WC}_1D.vCONFIG_VERSIONS.syst.MultiDimFit.mH120.root'
                fname_d = ddir+f'full_analysis/higgsCombine_Data.all_combined.{WC}_1D.vCONFIG_VERSIONS.syst.MultiDimFit.mH120.root'
            else:
                fname_a = ddir+f'full_analysis/higgsCombine_Asimov.all_combined.{WC}_All.vCONFIG_VERSIONS_NDIM.syst.MultiDimFit.mH120.root'
                fname_d = ddir+f'full_analysis/higgsCombine_Data.all_combined.{WC}_All.vCONFIG_VERSIONS_NDIM.syst.MultiDimFit.mH120.root'
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
            ####
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
            LL_a = LLs_interp_a[0]
            LL_d = LLs_interp_d[0]
            UL_a = ULs_interp_a[0]
            UL_d = ULs_interp_d[0]
            # also want range
            LL_a_r = np.min(LLs_interp_a[0])
            LL_d_r = np.min(LLs_interp_d[0])
            UL_a_r = np.max(ULs_interp_a[0])
            UL_d_r = np.max(ULs_interp_d[0])
            v_list = [LL_a, UL_a, LL_d, UL_d]
            s_list = []
            for v_ in v_list:
                s_ = []
                for v in v_:
                    s_.append(numerical_formatter(v))
                s_list.append(s_)
            WC_ = f'{WC}:'
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
        s_prints = np.array(s_prints)
        WC_bests_a = np.array(WC_bests_a)
        WC_bests_d = np.array(WC_bests_d)
        s_WC_bests_a = np.array(s_WC_bests_a)
        s_WC_bests_d = np.array(s_WC_bests_d)
        inds = np.arange(len(WCs))
        if freeze:
            # only generate sorting when freezing
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
        # temp dict
        result = {'s_prints': s_prints[inds_sort], 'WCs_sorted': WCs_sorted, 'pdiffs': s_pdiffs, 's_ULs_a': lscope['s_ULs_a'],
                  's_LLs_a': lscope['s_LLs_a'], 's_ULs_d': lscope['s_ULs_d'], 's_LLs_d': lscope['s_LLs_d'], 's_WC_bests_a': s_WC_bests_a[inds_sort],
                  's_WC_bests_d': s_WC_bests_d[inds_sort], 'meas_dicts': lscope['meas_dicts']}
        # add to main dict
        results_dict[freeze_str] = result
    return results_dict


# 4 column
#def make_summary_table(WCs, LLs_a, ULs_a , LLs_d, ULs_d, WCs_bests_a, WCs_bests_d, meas_dicts, dim='dim6', order_sens=True, tex_file=None):
def make_summary_table_lim(results_dict, dim='dim6', order_sens=True, tex_file=None):
    # Construct the LaTeX table as a string
    table = r"\begin{table}[hbtp!]" + "\n"
    table += r"\centering" + "\n"
    # caption
    if order_sens:
        #table += r"\label{tab:limit_summary_"+f"{dim}"+"_with_profile}" + "\n"
        # if dim == 'dim6':
        table += r"\topcaption{Summary of the 95\% \CL bounds on the dim-6 Wilson coefficients. We consider the case of a single varying Wilson coefficient (``Freeze other WCs"+'"'+r") as well as the case when the other Wilson coefficients are profiled (``Profile other WCs"+'"'+r"). The Wilson coefficients are ordered by increasing confidence interval width. \label{tab:limit_summary_"+f"{dim}"+"}}" + "\n"
    else:
        raise NotImplemented('order_sens=False is not implemented for this table. Try again.')
        # table += r"\topcaption{Summary of the 95\% \CL bounds and measurements on the dim-6 Wilson coefficients. We consider the case of a single varying Wilson coefficient (\"Freeze Other WCs\") as well as the case when the other Wilson coefficients are profiled over (``Profile Other WCs''). \label{tab:limit_summary_"+f"{dim}"+"_alt_order}}" + "\n"
    table += r"\begin{tabular}{r|c|c|c|c}" + "\n"
    table += r"\hline" + "\n"
    table += r"& \multicolumn{2}{p{7cm}|}{\centering Freeze other WCs} & \multicolumn{2}{p{7cm}}{\centering Profile other WCs} \\" + "\n"
    table += r"\hline" + "\n"
    table += r"Wilson & \multicolumn{2}{p{7cm}|}{\centering 95\% \CL Bounds $[\TeV^{-2}]$} & \multicolumn{2}{p{7cm}}{\centering 95\% \CL Bounds $[\TeV^{-2}]$} \\" + "\n"
    table += r"coefficient & \multicolumn{1}{p{3.5cm}|}{\centering Observed} & Expected & \multicolumn{1}{p{3.5cm}|}{\centering Observed} & Expected \\" + "\n"
    wc_suff = r'/\Lambda^{2}$'
    table += r"\hline" + "\n"

    # Add the rows to the table
    #nrows = len(results_dict['freeze']['WCs_sorted'])
    WCs = results_dict['Freeze']['WCs_sorted']
    rf = results_dict['Freeze']
    rp = results_dict['Profile']
    for i, WC in enumerate(WCs):
        WC_p = "$"+ WC_pretty_print_dict[WC] + wc_suff
        row = [WC_p]
        # freeze results
        d_str = []
        for L, U in zip(rf['s_LLs_d'][i], rf['s_ULs_d'][i]):
            d_str.append(f"$[{L}, {U}]$")
        d_str = r" $\cup$ ".join(d_str)
        a_str = []
        for L, U in zip(rf['s_LLs_a'][i], rf['s_ULs_a'][i]):
            a_str.append(f"$[{L}, {U}]$")
        a_str = r" $\cup$ ".join(a_str)
        meas_str = ' or '.join(rf['meas_dicts'][i]['Data']['tex_string_list'])
        row.append(d_str)
        row.append(a_str)
        #row.append(meas_str)
        # profile results
        d_str = []
        for L, U in zip(rp['s_LLs_d'][i], rp['s_ULs_d'][i]):
            d_str.append(f"$[{L}, {U}]$")
        d_str = r" $\cup$ ".join(d_str)
        a_str = []
        for L, U in zip(rp['s_LLs_a'][i], rp['s_ULs_a'][i]):
            a_str.append(f"$[{L}, {U}]$")
        a_str = r" $\cup$ ".join(a_str)
        meas_str = ' or '.join(rp['meas_dicts'][i]['Data']['tex_string_list'])
        row.append(d_str)
        row.append(a_str)
        #row.append(meas_str)
        table += ' & '.join(row) + '\\\\' + '\n'

    table += r"\hline" + "\n"
    table += r"\end{tabular}" + "\n"

    table += r"\end{table}" + "\n"

    print(table)

    if not tex_file is None:
        with open(tex_file, 'w') as f:
            f.write(table)
    return table

def make_summary_table_meas(results_dict, dim='dim6', order_sens=True, tex_file=None):
    # Construct the LaTeX table as a string
    table = r"\begin{table}[hbtp!]" + "\n"
    table += r"\centering" + "\n"
    # caption
    if order_sens:
        #table += r"\label{tab:limit_summary_"+f"{dim}"+"_with_profile}" + "\n"
        # if dim == 'dim6':
        # table += r"\topcaption{Summary of the measurements on the dim-6 Wilson coefficients. We consider the case of a single varying Wilson coefficient (``Freeze Other WCs'') as well as the case when the other Wilson coefficients are profiled over (``Profile Other WCs''). The Wilson coefficients are ordered by increasing confidence interval width. \label{tab:measurement_summary_"+f"{dim}"+"}}" + "\n"
        table += r"\topcaption{Summary of the measurements of the dim-6 Wilson coefficients. We consider the case of a single varying Wilson coefficient (``Freeze other WCs"+'"'+r") as well as the case when the other Wilson coefficients are profiled (``Profile other WCs"+'"'+r"). \label{tab:measurement_summary_"+f"{dim}"+"}}" + "\n"
    else:
        raise NotImplemented('order_sens=False is not implemented for this table. Try again.')
        # table += r"\topcaption{Summary of the 95\% \CL bounds and measurements on the dim-6 Wilson coefficients. We consider the case of a single varying Wilson coefficient (\"Freeze Other WCs\") as well as the case when the other Wilson coefficients are profiled over (``Profile Other WCs''). \label{tab:limit_summary_"+f"{dim}"+"_alt_order}}" + "\n"
    table += r"\begin{tabular}{r|c|c}" + "\n"
    table += r"\hline" + "\n"
    table += r"& \multicolumn{1}{p{4cm}|}{\centering Freeze other WCs} & \multicolumn{1}{p{4cm}}{\centering Profile other WCs} \\" + "\n"
    table += r"\hline" + "\n"
    table += r"Wilson & \multicolumn{1}{p{4cm}|}{\centering Measurement $[\TeV^{-2}]$} & \multicolumn{1}{p{4cm}}{\centering Measurement $[\TeV^{-2}]$} \\" + "\n"
    table += r"coefficient & Observed & Observed \\" + "\n"
    wc_suff = r'/\Lambda^{2}$'
    table += r"\hline" + "\n"

    # Add the rows to the table
    #nrows = len(results_dict['freeze']['WCs_sorted'])
    WCs = results_dict['Freeze']['WCs_sorted']
    rf = results_dict['Freeze']
    rp = results_dict['Profile']
    for i, WC in enumerate(WCs):
        WC_p = "$"+ WC_pretty_print_dict[WC] + wc_suff
        row = [WC_p]
        # freeze results
        d_str = []
        for L, U in zip(rf['s_LLs_d'][i], rf['s_ULs_d'][i]):
            d_str.append(f"$[{L}, {U}]$")
        d_str = r" $\cup$ ".join(d_str)
        a_str = []
        for L, U in zip(rf['s_LLs_a'][i], rf['s_ULs_a'][i]):
            a_str.append(f"$[{L}, {U}]$")
        a_str = r" $\cup$ ".join(a_str)
        meas_str = ' or '.join(rf['meas_dicts'][i]['Data']['tex_string_list'])
        #row.append(d_str)
        #row.append(a_str)
        row.append(meas_str)
        # profile results
        d_str = []
        for L, U in zip(rp['s_LLs_d'][i], rp['s_ULs_d'][i]):
            d_str.append(f"$[{L}, {U}]$")
        d_str = r" $\cup$ ".join(d_str)
        a_str = []
        for L, U in zip(rp['s_LLs_a'][i], rp['s_ULs_a'][i]):
            a_str.append(f"$[{L}, {U}]$")
        a_str = r" $\cup$ ".join(a_str)
        meas_str = ' or '.join(rp['meas_dicts'][i]['Data']['tex_string_list'])
        #row.append(d_str)
        #row.append(a_str)
        row.append(meas_str)
        table += ' & '.join(row) + '\\\\' + '\n'

    table += r"\hline" + "\n"
    table += r"\end{tabular}" + "\n"

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
                        help='Which dimension? ["dim6" (default)]')
    parser.add_argument('-o', '--OrderBySens',
                        help='Order by sensitivity? ["y" (default), "n" -- dim8 only so far]')
    args = parser.parse_args()
    if args.Dimension is None:
        dims = 'dim6'
    else:
        dims = args.Dimension
    if dims != 'dim6':
        raise ValueError('--Dimension must be "dim6" to make the table with profiled results.')
    # if dims == 'all':
    #     dims_list = ['dim6', 'dim8']
    # else:
    #     dims_list = [dims]
    dims_list = [dims]
    if args.OrderBySens is None:
        order_sens = True
    else:
        order_sens = args.OrderBySens == 'y'

    dim_dict = {'dim6': dim6_WCs,
                #'dim8': dim8_WCs_sort_AN,
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
    results_dict_dim = {}
    print('Limits with systematics...')
    for dim in dims_list:
    #for dim in ['dim6', 'dim8']:
    #for dim in ['cW_test']:
    # for dim in ['dim6', 'dim8_partial']:
        print(f'{dim} Current Limit Ranking (full analysis):')
        _ = print_summary_table_lim_sorted(ddir, dim, dim_dict, order_sens=order_sens)
        results_dict_dim[dim] = _
        print('\n')

    # make tables, with systematics
    for dim in dims_list:
        # limits
        if order_sens:
            tex_file = plotdir+f'limit_summary_{dim}.tex'
        else:
            tex_file = plotdir+f'limit_summary_{dim}_alt_order.tex'
        make_summary_table_lim(results_dict_dim[dim], dim=dim, order_sens=order_sens, tex_file=tex_file)
        # measurements
        if order_sens:
            tex_file = plotdir+f'measurement_summary_{dim}.tex'
        else:
            tex_file = plotdir+f'measurement_summary_{dim}_alt_order.tex'
        make_summary_table_meas(results_dict_dim[dim], dim=dim, order_sens=order_sens, tex_file=tex_file)
