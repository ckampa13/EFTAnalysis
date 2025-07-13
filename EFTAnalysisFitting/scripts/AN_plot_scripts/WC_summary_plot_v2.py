# This is a copy of "WC_summary_plot_v2.py". I want to add the feature
# to scale the limits on the less sensitive WCs down so that the plots are
# visually easier to read.
import os
import argparse
from copy import deepcopy
import numpy as np
# from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
#from limit_summary_plot_from_dir import make_limit_summary_plot
from CONFIG_VERSIONS import WC_ALL
from MISC_CONFIGS import (
    datacard_dir,
    template_outfilename,
    dim6_ops,
    #WC_pretty_print_dict,
    WC_pretty_print_dict_AN,
    SR_pretty_print_dict_AN,
)
WC_pretty_print_dict = WC_pretty_print_dict_AN
SR_pretty_print_dict = SR_pretty_print_dict_AN
#from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, get_lims_quad_interp, CL_1sigma
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title, numerical_formatter

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True

#WIDTH_MAX = 5
#RESCALE_FACTOR = 0.1

#WIDTH_MAX = 15
#RESCALE_FACTOR = 0.05

rescale_dict = {
    'dim6': {
        #'WIDTH_MAX': 15.,
        #'RESCALE_FACTOR': 0.05,
        'WIDTH_MAX': 5.,
        'RESCALE_FACTOR': 0.01
    },
    'dim8': {
        'WIDTH_MAX': 5.,
        'RESCALE_FACTOR': 0.1
    },
}

# FIXME! Harmonize with the function in "limit_summary_plot_from_dir.py"
# main feature that would need to change is passing in multiple WCs
# which should be embedded in root_file_dict_full
def make_limit_summary_plot_WCs(root_file_dict_full, title, CL=0.95, add_hrule=False, plot_stat_only=True, xlim_factor=2.0, fixed_xlim=None, savefile=None, sort_by_lim=True,
                                plot_var_of_choice=False, title_on=False, top_6=True, WIDTH_MAX=5., RESCALE_FACTOR=0.1, Asimov=True):
    # bottom to top, plots 0, 1, 2, 3, ....
    # plot
    # if plot_var_of_choice:
    #     fig = plt.figure(figsize=(16, 8))
    #     ax = fig.add_axes([0.15, 0.1, 0.55, 0.8])
    # # TEST BELOW
    # else:
    #     ks = list(root_file_dict_full.keys())
    #     # print(ks)
    #     # print(ks[0])
    #     if root_file_dict_full[ks[0]]['WC'] in dim6_ops:
    #         height = 8
    #         yfrac = 0.8
    #         y0 = 0.1
    #     else:
    #         height = 4
    #         yfrac = 0.5
    #         y0 = 0.25
    #     fig = plt.figure(figsize=(14, height))
    #     ax = fig.add_axes([0.05, y0, 0.75, yfrac])
    #if len(root_file_dict_full) <= 6:
    if Asimov:
        stat_color = 'magenta'
    else:
        stat_color = 'lime'
    N_rescaled = 0
    #N_rescaled_s = 0
    if top_6:
        fig, ax = plt.subplots(figsize=(12, 8))
    else:
        if len(root_file_dict_full) > 15:
            fig, ax = plt.subplots(figsize=(12, 16))
        else:
            fig, ax = plt.subplots(figsize=(12, 12))
    #fig.set_constrained_layout_pads(h_pad=0.0417, w_pad=0.0417) # default
    fig.set_constrained_layout_pads(h_pad=0.0417, w_pad=0.075)
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    # loop through files to plot
    LLs_all = []
    ULs_all = []
    yvals_all = []
    ylabels_all = []
    text_annot_all = []
    var_annot_all = []
    widths_to_rescale = []
    xlim_track = 0.
    # for sorting
    # C_best_list = []
    # yval_list = []
    # xerr_list = []
    #y_sort_dict = {}
    rdict_full = deepcopy(root_file_dict_full)
    for loop in [0, 1]:
        if loop == 0:
            errs_list = []
            ys_start_list = []
        if loop == 1:
            # sort
            if sort_by_lim:
                inds = np.argsort(errs_list)[::-1]
                ys_start_list = np.array(ys_start_list)
                #ys_new_list = np.array(ys_start_list)[inds]
                ys_new_list = ys_start_list[inds]
                y_sort_dict = {yold:ynew for yold,ynew in zip(ys_start_list, ys_new_list)}
                #
                rdict_full_ = deepcopy(rdict_full)
                rdict_full = {}
                for y_old, y_new in y_sort_dict.items():
                    #rdict_full[y_new] = rdict_full_[y_old]
                    rdict_full[y_old] = rdict_full_[y_new]
        for i, item in enumerate(sorted(rdict_full.items())):
            plot_dict = {}
            if i==1:
                #label_total = r'Proj. (stat. $\bigoplus$ syst.)'+'\nAsimov Dataset'
                #label_stat = 'stat. only'
                #label_total = 'With Systematics\nAsimov Dataset'
                #label_stat = 'Statistical Uncertainties Only'
                label_total = 'With Systematics\n'
                if Asimov:
                    label_total += 'Asimov Dataset'
                else:
                    label_total += 'Data'
                label_stat = 'Statistical Uncertainties Only'
            else:
                label_total = None
                label_stat = None
            yval, info_dict = item
            WC = info_dict['WC']
            if loop == 1:
                yvals_all.append(yval)
            root_file_dict = info_dict['root_file_dict']
            if loop == 1:
                ylabels_all.append(info_dict['ylabel'])
            var_of_choice = info_dict['variable_of_choice']
            # get limits and plot
            # total
            # Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC)
            # Cs_s, NLL_s, CL_list_s, NLL_cuts_s, LLs_s, ULs_s, C_best_stat_s, NLL_best_s = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC)
            if Asimov:
                hold = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
            else:
                #hold = get_lims([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
                hold = get_lims_quad_interp([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True, kind='linear')
            Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
            if Asimov:
                hold = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
            else:
                #hold = get_lims([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
                hold = get_lims_quad_interp([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True, kind='linear')
            Cs_s, NLL_s, CL_list_s, NLL_cuts_s, _, _, LLs_s, ULs_s, C_best_s, NLL_best_s = hold
            Nlims = len(ULs[0])
            Nlims_s = len(ULs_s[0])
            Nlims_max = np.max([Nlims, Nlims_s])
            err_low = C_best - LLs[0][0]
            err_high = ULs[0][-1] - C_best
            err_low_s = C_best_s - LLs_s[0][0]
            err_high_s = ULs_s[0][-1] - C_best_s
            if loop == 0:
                W_rs = (ULs[0][-1] - LLs[0][0]) > WIDTH_MAX
                widths_to_rescale.append(W_rs)
                if W_rs:
                    x_max = RESCALE_FACTOR*max(abs(ULs[0][-1]), abs(LLs[0][0]))
                else:
                    x_max = max(abs(ULs[0][-1]), abs(LLs[0][0]))
                xlim_track = max(xlim_track, x_max)
            # add to annotation
            if abs(np.round(C_best, 3)) < 0.001:
                best_str = f'{0.0:0.3f}'
            else:
                #best_str = f'{C_best:0.3f}'
                best_str = numerical_formatter(C_best)
            if abs(np.round(C_best_s, 3)) < 0.001:
                best_str_s = f'{0.0:0.3f}'
            else:
                #best_str = f'{C_best:0.3f}'
                best_str_s = numerical_formatter(C_best_s)
            # text_annot = rf'${best_str}\ ~^{{+ {err_high:0.3f} }}_{{- {err_low:0.3f} }}$'
            # text_annot += rf'$\ ~^{{+ {err_high_s:0.3f} }}_{{- {err_low_s:0.3f} }}$'
            # numerical formatter
            #best_str = numerical_formatter(C_best)
            s_high = '+'+numerical_formatter(err_high)
            s_low = '-'+numerical_formatter(err_low)
            s_high_s = '+'+numerical_formatter(err_high_s)
            s_low_s = '-'+numerical_formatter(err_low_s)
            text_annot = rf'${best_str}\ ~^{{ {s_high} }}_{{ {s_low} }}$'
            ls = [len(s_high), len(s_low)]
            # if (max(ls) < 5) and (max(abs(err_high), abs(err_low)) < 100):
            #     text_annot += r'$\ $'
            if Asimov:
                text_annot += rf'$\ \ ~^{{ {s_high_s} }}_{{ {s_low_s} }}$'
            #text_annot += rf'$\ {best_str_s}\ ~^{{ {s_high_s} }}_{{ {s_low_s} }}$'
            if len(LLs[0]) > 1:
                # asterisk will be explained in figure caption (means discontinuous interval)
                text_annot += '  *'
            # use width of the limit for sorting
            err_mean = (ULs[0][-1] - LLs[0][0])
            if loop == 0:
                errs_list.append(err_mean)
                ys_start_list.append(yval)
            if loop == 1:
                # debug
                N_to_rescale = np.sum(widths_to_rescale)
                print(f'{i}, {WC}, N_to_rescale={N_to_rescale}')
                # TEST
                err_high_annot = -1000
                err_low_annot = -1000
                # decide whether we rescale
                add_hrule_scale = False
                if (ULs[0][-1] - LLs[0][0]) > WIDTH_MAX:
                    to_rescale = True
                    print(f'{i}, {WC}, will be rescaled...')
                    print(f'i={i}, N_to_rescale={N_to_rescale}')
                    if i == (N_to_rescale-1):
                        add_hrule_scale = True
                    else:
                        add_hrule_scale = False
                    N_rescaled += 1
                else:
                    to_rescale = False
                # find the interval that the best val is actually in
                #for UL_, LL_, UL_s, LL_s in zip(ULs[0], LLs[0], ULs_s[0], LLs_s[0]):
                for i in range(Nlims_max):
                    try:
                        UL_ = ULs[0][i]
                        LL_ = LLs[0][i]
                    except:
                        UL_ = ULs[0][-1]
                        LL_ = LLs[0][-1]
                    try:
                        UL_s = ULs_s[0][i]
                        LL_s = LLs_s[0][i]
                    except:
                        UL_s = ULs_s[0][-1]
                        LL_s = LLs_s[0][-1]
                    # for UL_, LL_ in zip(UL, LL):
                    to_plot = False
                    to_plot_s = False
                    if (C_best > LL_) and (C_best < UL_):
                        to_plot = True
                    if (C_best_s > LL_s) and (C_best_s < UL_s):
                        to_plot_s = True
                    if to_rescale:
                    #if (UL_-LL_) > WIDTH_MAX:
                        #if N_rescaled == 0:
                        # print(f'{i}, {WC}, will be rescaled...')
                        # print(f'i={i}, N_to_rescale={N_to_rescale}')
                        # if i == (N_to_rescale-1):
                        #     add_hrule_scale = True
                        # else:
                        #     add_hrule_scale = False
                        #N_rescaled += 1
                        print('Rescaling!')
                        print(f'C_best={C_best}, LL_={LL_}, LL_s={LL_s}, UL_={UL_}, UL_s={UL_s}')
                        #C_best *= RESCALE_FACTOR
                        #C_best_s *= RESCALE_FACTOR
                        C_best_sc = RESCALE_FACTOR * deepcopy(C_best)
                        C_best_sc_s = RESCALE_FACTOR * deepcopy(C_best_s)
                        LL_ *= RESCALE_FACTOR
                        LL_s *= RESCALE_FACTOR
                        UL_ *= RESCALE_FACTOR
                        UL_s *= RESCALE_FACTOR
                        # Cs to be rescaled?
                        Cs_sc = RESCALE_FACTOR * deepcopy(Cs)
                        Cs_s_sc = RESCALE_FACTOR * deepcopy(Cs_s)
                        print(f'C_best={C_best}, LL_={LL_}, LL_s={LL_s}, UL_={UL_}, UL_s={UL_s}')
                    else:
                        C_best_sc = deepcopy(C_best)
                        C_best_sc_s = deepcopy(C_best_s)
                        Cs_sc = deepcopy(Cs)
                        Cs_s_sc = deepcopy(Cs_s)



                    err_low = C_best_sc - LL_
                    err_high = UL_ - C_best_sc
                    err_low_s = C_best_sc_s - LL_s
                    err_high_s = UL_s - C_best_sc_s
                    if to_plot:
                        print(f'C_best_sc={C_best_sc}, yval={yval}, err_low={err_low}, err_high={err_high}')
                        ax.errorbar([C_best_sc],[yval], xerr=[[err_low],[err_high]], c='black', capsize=8.0, linestyle='-', linewidth=2, capthick=2, markersize=16, marker='.', zorder=8, label=label_total)
                    if plot_stat_only:
                        if to_plot_s:
                            print(f'C_best_sc_s={C_best_sc_s}, yval={yval}, err_low_s={err_low_s}, err_high_s={err_high_s}')
                            ax.errorbar([C_best_sc_s], [yval], xerr=[[err_low_s],[err_high_s]], c=stat_color, capsize=0., linestyle='-', linewidth=6, zorder=7, label=label_stat)
                    if add_hrule_scale:
                        # debug
                        print(f'Adding hrule for {WC}, where we start scaling.')
                        ax.plot([-500, 500], 2*[yval+0.5], '-', color='darkblue', linewidth=2)
                        ax.annotate(f'Limit x{RESCALE_FACTOR:0.2f}', (-xlim_track, yval), (-xlim_track, yval), xycoords='data', wrap=False, verticalalignment='center', zorder=100)
                    # an additional interval to plot
                    #else:
                        # if to_rescale:
                        #     C_best *= RESCALE_FACTOR
                        #     C_best_s *= RESCALE_FACTOR
                        #     LL_ *= RESCALE_FACTOR
                        #     LL_s *= RESCALE_FACTOR
                        #     UL_ *= RESCALE_FACTOR
                        #     UL_s *= RESCALE_FACTOR
                        #     # Cs to be rescaled?
                        #     Cs *= RESCALE_FACTOR
                        #     Cs_s *= RESCALE_FACTOR
                        #cval = (UL_ + LL_) / 2.
                    print('Trying to plot extra interval (syst)...')
                    try:
                        m = (Cs_sc >= LL_) & (Cs_sc <= UL_)
                        ibest = np.argmin(NLL[m])
                        if WC == 'cHl3':
                            print(ibest)
                            print(Cs_sc[m], NLL[m])

                        cval = Cs_sc[m][ibest]
                        err_low = cval - LL_
                        err_high = UL_ - cval
                        print(f'cval={cval}, yval={yval}, LL_={LL_}, UL_={UL_}, err_low={err_low}, err_high={err_high}')
                        ax.errorbar([cval], [yval], xerr=[[err_low],[err_high]], c='black', capsize=8.0, linestyle='-', linewidth=2, capthick=2, marker='', zorder=8)
                    except:
                        pass
                        print('Could not plot extra interval (syst)...')
                    print('Trying to plot extra interval (stat)...')
                    try:
                        m_s = (Cs_sc_s >= LL_s) & (Cs_sc_s <= UL_s)
                        ibest_s = np.argmin(NLL_s[m_s])
                        cval_s = Cs_sc_s[m_s][ibest_s]
                        err_low_s = cval_s - LL_s
                        err_high_s = UL_s - cval_s
                        if plot_stat_only:
                            print(f'cval_s={cval_s}, yval={yval}, LL_s={LL_s}, UL_s={UL_s}, err_low_s={err_low_s}, err_high_s={err_high_s}')
                            ax.errorbar([cval_s], [yval], xerr=[[err_low_s],[err_high_s]], c='magenta', capsize=0., linestyle='-', linewidth=6, zorder=7)
                    except:
                        pass
                        print('Could not plot extra interval (stat)...')
                LLs_all.append(LLs[0][0])
                ULs_all.append(ULs[0][-1])
                text_annot_all.append(text_annot)
                var_annot_all.append(var_of_choice)
    # axis labels
    # this will grab most recent WC (fine as long as I don't mix dim6 and dim8 on the same plot)
    if WC in dim6_ops:
        suff = r'$ / \Lambda^2$ [TeV]$^{-2}$'
        dim = 'Dimension-6'
    else:
        suff = r'$ / \Lambda^4$ [TeV]$^{-4}$'
        dim = 'Dimension-8'
    #WC_lab = WC_pretty_print_dict[WC]
    ##ax.set_xlabel('Sensitivity to '+dim+' Wilson Coefficients'+suff)
    ax.set_xlabel(f'{CL*100:0.0f}\% CL Limits')
    if title_on:
        ax.set_title(title+'\n', pad=3.)
    # set xlim to be symmetric
    LLs_all = np.array(LLs_all)
    ULs_all = np.array(ULs_all)
    if xlim_factor is None:
        # xlim = np.max(np.abs(fixed_xlim))
        xlim = np.min(np.abs(fixed_xlim))
        ax.set_xticks(np.arange(round(-xlim-1), round(xlim+1)+1))
        ax.set_xlim(fixed_xlim)
    else:
        #xlim = xlim_factor*np.max(np.abs([LLs_all, ULs_all]))
        xlim = xlim_factor * xlim_track
        ax.set_xticks(np.arange(round(-xlim-1), round(xlim+1)+1))
        ax.set_xlim([-xlim, xlim])
    # add dummy point above top for label space and below for aesthetics
    yvals = sorted(root_file_dict_full.keys())
    yrange = np.max(yvals) - np.min(yvals)
    if top_6:
        ax.scatter([0.], [np.max(yvals) + 0.30 * yrange], s=0., alpha=0.)
        ax.scatter([0.], [np.min(yvals) - 0.1 * yrange], s=0., alpha=0.)
    else:
        ax.scatter([0.], [np.max(yvals) + 0.15 * yrange], s=0., alpha=0.)
        ax.scatter([0.], [np.min(yvals) - 0.02 * yrange], s=0., alpha=0.)
    # add rule between combined and others
    if add_hrule:
        yhrule = (yvals[-1] + yvals[-2]) / 2.
        ax.plot(ax.get_xlim(), [yhrule, yhrule], '--', c='gray', alpha=0.8)
    # annotations for sensitivity
    for yval, text_annot, var_annot in zip(yvals, text_annot_all, var_annot_all):
        ax.annotate(text_annot, (1.0*xlim, yval), (1.05*xlim, yval), xycoords='data', wrap=False, verticalalignment='center', zorder=100)
        if plot_var_of_choice:
            ax.annotate(var_annot, (1.0*xlim, yval), (1.65*xlim, yval), xycoords='data', wrap=False, verticalalignment='center', zorder=100)
    # additional annotations
    # total, stat
    if Asimov:
        header_str = r'best$\ \ \ \ $total$\ \ \ $stat.'
    else:
        header_str = r'best$\ \ \ \ $total'
    header_y = np.min([np.max(yvals) + 0.5, np.max(yvals) + 0.30 * yrange])
    #ax.annotate(header_str, (1.00*xlim, header_y), (1.22*xlim, header_y), xycoords='data')
    ax.annotate(header_str, (1.00*xlim, header_y), (1.05*xlim, header_y), xycoords='data')
    if plot_var_of_choice:
        var_header_str = 'Variable of\nchoice'
        ax.annotate(var_header_str, (1.00*xlim, header_y),  (1.65*xlim, header_y), xycoords='data')
    # formatting
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax = ticks_in(ax)
    ax = ticks_sizes(ax, major={'L':10,'W':1.1}, minor={'L':4,'W':0.8})
    ax.set_yticks(yvals)
    ax.set_yticklabels(ylabels_all)
    #ax.set_xticks(np.arange(round(-xlim-1), round(xlim+1)+1))
    # only want vertical grid lines
    ax.grid(axis='y')
    # ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    #ax.legend(loc='upper left')
    ax.legend(loc='upper left', fontsize=20.0)
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax


def run_plot_WC_summary(WCs, CL, ScanType, plot_stat_only, xlim_factor, fixed_xlim, top_6, Asimov, Unblind):
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_full = os.path.join(dcdir, 'output', 'full_analysis')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'full_analysis')
    root_file_dict_full = {}
    # version & bin info fixed for all WC
    version = 'vCONFIG_VERSIONS'
    bin_info = {'output_dir': output_dir_full, 'plot_dir': plot_dir,
                'channel': 'All', 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    # construct root file for each WC
    for i, WC in enumerate(WCs):
        WC_l = WC_pretty_print_dict[WC]
        file_syst = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
        file_stat = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
        root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
        root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
        root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
        root_file_dict_full[i] = {'root_file_dict': root_file_dict, 'ylabel': WC_l,
                                   'variable_of_choice': '', 'WC': WC}
    # check dim6 or dim8 based on final entry
    if WC in dim6_ops:
        dim = 'dim6'
        dim_l = 'Dimension-6'
    else:
        dim = 'dim8'
        dim_l = 'Dimension-8'
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    if top_6:
        plotfile = os.path.join(plot_dir, f'{asi_prestr}{dim}_sensitivity_summary{stat_str}{ScanType}_top6_v2')
    else:
        plotfile = os.path.join(plot_dir, f'{asi_prestr}{dim}_sensitivity_summary{stat_str}{ScanType}_v2')
    title = f'{int(CL*100)}\% CL Sensitivity to '+dim_l+f' Wilson Coefficients {scan_title}'

    fig, ax = make_limit_summary_plot_WCs(root_file_dict_full, title, CL=CL, add_hrule=False, plot_stat_only=plot_stat_only,
                                          xlim_factor=xlim_factor, fixed_xlim=fixed_xlim, savefile=plotfile,
                                          sort_by_lim=True, plot_var_of_choice=False, top_6=top_6, WIDTH_MAX=rescale_dict[dim]['WIDTH_MAX'], RESCALE_FACTOR=rescale_dict[dim]['RESCALE_FACTOR'], Asimov=Asimov)

    return fig, ax


if __name__=='__main__':
    # FIXME! make this a commandline arg?
    # most sensitive
    # WCs_dim6 =  ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW']
    # all dim6
    #WCs_dim6 =  ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW', 'cHB', 'cHl3', 'cHWB', 'cll1', 'cHDD', 'cHbox']
    #WCs_dim8 = ['cT0', 'cM0']
    # all
    # WCs = WC_ALL
    # CL
    CL = 0.95
    # which scan type?
    # freeze all but one
    ScanType = '_1D'
    # profile
    #ScanType = '_All'
    # list of stat on / stat off
    #pstats = [False] # only make the plot without stat only
    pstats = [True] # only make the plot that includes stat only
    # pstats = [True, False] # both
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "top_6", ...]')
    parser.add_argument('-d', '--Dim',
                        help='dim6 or dim8? ["dim6" (default), "dim8"]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'all'
    top_6 = False
    if args.WC == 'all':
        WCs_full = WC_ALL
    elif args.WC == 'top_6':
        # FIXME! Update with top 6 dim8
        WCs_full = ['cW', 'cHq3', 'cHq1', 'cHu', 'cHd', 'cHW', 'cT0', 'cM0']
        top_6 = True
    else:
        WCs_full = [args.WC]
    if args.Dim is None:
        dim_arg = 'dim6'
    else:
        dim_arg = args.Dim
    if dim_arg == 'dim6':
        dim6 = True
    else:
        dim6 = False
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        Asimov = True
    else:
        Asimov = False
    if args.Unblind is None:
        args.Unblind = 'n'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    # make correct dim list
    WCs_dim = []
    for WC in WCs_full:
        if dim6:
            if WC in dim6_ops:
                WCs_dim.append(WC)
        else:
            if not WC in dim6_ops:
                WCs_dim.append(WC)
    # loop through dim6 and dim8
    #for WCs, dim in zip([WCs_dim6, WCs_dim8], ['dim6', 'dim8']):
    #for WCs, dim in zip([WCs_dim6], ['dim6']): # only dim6
    for WCs, dim in zip([WCs_dim], [dim_arg]): # only dim selected in args
        # run plot twice (with and without stat only)
        print("=========================================================")
        print(f"Making sensitivity plots for {dim}...")
        for pstat in pstats:
            print(f'Include stat-only? {pstat}')
            fig, ax = run_plot_WC_summary(WCs, CL=CL, ScanType=ScanType, plot_stat_only=pstat, xlim_factor=1.2, fixed_xlim=None, top_6=top_6,
                                          Asimov=Asimov, Unblind=Unblind)
            # fig, ax = run_plot_WC_summary(WCs, CL=CL, plot_stat_only=pstat, xlim_factor=None, fixed_xlim=[-1.5, 1.5])
        print("=========================================================\n")

