# same as NLL_limits_plot_from_dir.py, but adds full likelihood & channel breakdown
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import argparse
from copy import deepcopy
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import (
    datacard_dir,
    #template_filename,
    template_outfilename,
    #template_outfilename_stub,
    dim6_ops,
    #WC_pretty_print_dict,
    WC_pretty_print_dict_AN,
    SR_pretty_print_dict_AN,
)
WC_pretty_print_dict = WC_pretty_print_dict_AN
SR_pretty_print_dict = SR_pretty_print_dict_AN
#from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title, numerical_formatter

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True

#colors_list = ['black', 'red', 'green', 'blue', 'purple', 'orange']

colors_list = ['black', 'red', 'green', 'blue', 'purple', 'orange', 'magenta', 'saddlebrown', 'dimgray', 'cyan']

colors_dict = {'0L_2FJ': 'green', '0L_3FJ': 'blue', '1L_2FJ': 'magenta',
               '2L_OS': 'darkorange', '2L_OS_2FJ': 'cyan', '2L_SS': 'saddlebrown',
               '0L_2FJ_1T': 'gold', '1L_1FJ_1T': 'limegreen', '2L_0FJ_1T': 'dimgray'}

N_ch = len(colors_dict) + 1

def make_limit_NLL_summary_plot(WC, root_file_dict_full, title, CL_list=[0.95], plot_stat_only=False, savefile=None, sort_by_lim=True, ncol=2, legend=True, title_on=False, SignalInject=False):
    # plot
    # if ncol <= 2:
    #     fig = plt.figure(figsize=(16, 8))
    #     #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    #     ax = fig.add_axes([0.05, 0.1, 0.50, 0.75])
    # else:
    #     fig = plt.figure(figsize=(18, 8))
    #     ax = fig.add_axes([0.05, 0.1, 0.45, 0.75])
    #fig, axs = plt.subplots(1, 2, figsize=(20, 12), gridspec_kw={'width_ratios': [2., 1.5]})
    #ax, ax_leg = axs
    #ax_leg.axis('off')
    #fig, ax = plt.subplots(figsize=(18, 18))
    if not SignalInject:
        fig, ax = plt.subplots(figsize=(12, 12))
    else:
        fig, ax = plt.subplots(figsize=(12, 14))
    #fig, ax = plt.subplots()
    fig.set_constrained_layout_pads(h_pad=0.075, w_pad=0.0417)
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    # loop through files to plot
    LLs_all = []
    ULs_all = []
    yvals_all = []
    ylabels_all = []
    ymax_min = 100.
    # legend_labels_all = []
    # text_annot_all = []
    # var_annot_all = []
    rdict_full = deepcopy(root_file_dict_full)
    for loop in [0, 1]:
        if loop == 0:
            errs_list = []
            ys_start_list = []
        if loop == 1:
            # sort
            if sort_by_lim:
                inds = np.argsort(errs_list)#[::-1]
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
            yval, info_dict = item
            if loop == 1:
                yvals_all.append(yval)
            root_file_dict = info_dict['root_file_dict']
            if loop == 1:
                ylabels_all.append(info_dict['ylabel'])
            # get limits and plot
            # total
            hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
            Cs, NLL, CL_list_, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
            # err_low = C_best - LLs[0]
            # err_high = ULs[0] - C_best
            # # use width of the limit for sorting
            # err_mean = (ULs[0] - LLs[0])
            # multi interval
            err_low = C_best - LLs[0][0]
            err_high = ULs[0][-1] - C_best
            # use width of the limit for sorting
            err_mean = (ULs[0][-1] - LLs[0][0])
            if loop == 0:
                errs_list.append(err_mean)
                ys_start_list.append(yval)
            if loop == 1:
                # do actual plotting in second iteration
                # thicker total lim
                if i == 0:
                    #lw = 2.
                    lw = 3.
                else:
                    #lw = 1.
                    lw = 2.
                zorder = N_ch + 10 - i
                ##label_NLL = info_dict['ylabel']+f'\n'
                if 'Full analysis' in info_dict['ylabel']:
                    ch_l = info_dict['ylabel']
                    color = 'black'
                else:
                    ch_ = info_dict['ylabel']
                    #ch_ = rdict_full['bin_info']['channel']
                    ch_l = SR_pretty_print_dict[ch_]
                    color = colors_dict[ch_]
                label_NLL = ch_l + '\n'
                # label_NLL += f'[{LLs[0]:0.3f}, {ULs[0]:0.3f}]\n'
                # multi interval
                #label_NLL += '\n'.join([f'[{LL:0.3f}, {UL:0.3f}]' for LL, UL in zip(LLs[0], ULs[0])]) + '\n'
                # multi interval, numerical formatter
                label_NLL += '\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])]) + '\n'
                if (i + 1) % 2 == 0:
                    ls = ':'
                    lw *= 2.0
                else:
                    ls = '-'
                ax.plot(Cs, NLL, c=color, linestyle=ls, linewidth=lw, label=label_NLL, zorder=zorder)
                if plot_stat_only:
                    hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
                    Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, _, _, LLs_stat, ULs_stat, C_best_stat, NLL_best_stat = hold
                    #label_NLL = f'[{LLs_stat[0]:0.3f}, {ULs_stat[0]:0.3f}]\n(stat. only)\n'
                    # multi interval
                    #label_NLL = '\n'.join([f'[{LL:0.3f}, {UL:0.3f}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])]) + '\n(stat. only)\n'
                    # multi interval, numerical formatter
                    label_NLL += '\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])]) + '\n(stat. only)\n'
                    ax.plot(Cs_stat, NLL_stat, c=colors_list[i], linestyle='-.', linewidth=lw, label=label_NLL)
                # track limits for the x limits later
                LLs_all.append(LLs[0])
                ULs_all.append(ULs[0])
                # ylims
                #ymax_min = min(np.max(NLL), ymax_min)
    # plot the horizontal line for NLL_cut only once at the end
    xmin = np.min(Cs)
    xmax = np.max(Cs)
    xra = (xmax - xmin)
    #xmin -= xra*0.1
    #xmax += xra*0.1
    for NLL_cut, ls in zip(NLL_cuts, ['-', '-.']):
        #NLL_cut = NLL_cuts[0]
        #label = WC_l+f'@{CL*100:0.1f}\% CL'
        #label = r'$\Delta$NLL Threshold' + f'\n{int(CL*100):d}\% CL'
        label = r'$\Delta$NLL Threshold' + f'\n{int(CL_list[0]*100):d}\% CL'
        ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls, linewidth=2, label=label, zorder=100)
    # axis labels
    if WC in dim6_ops:
        suff = r'$ / \Lambda^2$ [TeV$^{-2}$]'
    else:
        suff = r'$ / \Lambda^4$ [TeV$^{-4}$]'
    if WC == 'sm':
        suff = r' ($\mu_{\mathrm{SM}}$)'
    ax.set_xlabel(WC_l+suff, fontweight ='bold', loc='right', labelpad=-2.0)#, fontsize=20.)
    ax.set_ylabel(r'$\Delta$NLL', fontweight='bold', loc='top')#, fontsize=20.)
    if title_on:
        ax.set_title(title+'\n', pad=3.)
    # ticks
    ax = ticks_in(ax)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax = ticks_sizes(ax, major={'L':15,'W':1.5}, minor={'L':8,'W':1})
    # set xlim to be symmetric
    # LLs_all = np.array(LLs_all)
    # ULs_all = np.array(ULs_all)
    if WC == 'sm':
        #ax.set_xlim([xmin, xmax])
        ax.set_xlim([-0.5, xmax])
    else:
        xlim_factor = 2.
        xlim = xlim_factor*np.max(np.abs(np.concatenate([np.concatenate([LL for LL in LLs_all]), np.concatenate([UL for UL in ULs_all])])))
        ax.set_xlim([-xlim, xlim])
        # FIXME! for tau debug
        max_ = 10*np.min(np.abs(np.concatenate([UL for UL in ULs_all])))
        #max_ = 100.
        if xlim > max_:
            ax.set_xlim([-max_, max_])
    if SignalInject:
        iv = abs(InjectValue)
        ax.set_xlim([-1.5*iv, 1.5*iv])
    #ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    if ymax_min > 2.5*np.max(NLL_cuts):
        yu = 2.5 * np.max(NLL_cuts)
    else:
        yu = ymax_min
    ax.set_ylim([-0.01, yu])
    #if WC == 'sm':
    #    ax.set_ylim([-0.01, 3.])
    if legend:
        ###ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=ncol)
        #ax.legend(loc='upper left', bbox_to_anchor=(0.0,-0.1), ncol=3)
        #ax.legend(loc='upper left', bbox_to_anchor=(0.0,-0.15), ncol=3, fontsize=18.0,
        #          borderpad=10.0)
        if (not SignalInject) and (not WC == 'sm'):
            #fig.legend(loc='outside lower left', ncol=3, fontsize=20.0)
            fig.legend(loc='outside lower left', ncol=4, fontsize=20.0)
        else:
            #fig.legend(loc='outside lower left', ncol=3, fontsize=18.0)
            #fig.legend(loc='outside lower left', ncol=4, fontsize=18.0)
            fig.legend(loc='outside lower left', ncol=4, fontsize=20.0)
        # separate axis
        #handles, labels = ax.get_legend_handles_labels()
        #ncol_ = ncol
        #ncol_ = 6
        #ax_leg.legend(handles, labels, loc='upper left', clip_on=True)#, ncol=ncol_)
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        #fig.savefig(savefile+'.png')
    return fig, ax

def run_NLL_plot_analysis_channel(WC, datacard_dict, CL_list, plot_stat_only, SignalInject=False, InjectValue=0.0, ScanType='_1D', expect_signal='1', legend=True):
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    if SignalInject:
        Asi = f'Data_SignalInject_{WC}'
    else:
        Asi = 'Asimov'
    # custom SM
    if WC == 'sm':
        scan_dir = ''
        ScanType = ''
        if expect_signal is None:
            expect_signal = '0'
        scan_title = f'(Expected Signal = {expect_signal})'
        Asi += f'_expect_signal_{expect_signal}'
        SignalInject = False

    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    output_dir_ch = os.path.join(datacard_dir, 'output', 'channel')
    output_dir_full = os.path.join(datacard_dir, 'output', 'full_analysis')
    plot_dir = os.path.join(datacard_dir, 'AN_plots', 'full_analysis', scan_dir)
    root_file_dict_full = {}
    # construct root file for each channel
    for i, ch in enumerate(sorted(datacard_dict.keys())):
        WCs = versions_dict[ch]['EFT_ops'] + ['sm']
        if not WC in WCs:
            continue
        fname_ch = datacard_dict[ch]['info']['file_name']
        sname_ch = datacard_dict[ch]['info']['short_name']
        v = versions_dict[ch]['v']
        version = f'v{v}'
        bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                    #'channel': fname_ch, 'subchannel': 'All',
                    'channel': sname_ch, 'subchannel': 'All',
                    'version': version, 'bin_': 'All',
                    }
        file_syst = template_outfilename.substitute(asimov=Asi, channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
        file_stat = template_outfilename.substitute(asimov=Asi, channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
        root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
        root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
        root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
        root_file_dict_full[i] = {'root_file_dict': root_file_dict, 'ylabel': sname_ch,
                                  'variable_of_choice': datacard_dict[ch]['info']['variable_of_choice']}
    # construct root file for full analysis
    N = len(datacard_dict.keys())-1
    version = 'vCONFIG_VERSIONS'
    bin_info = {'output_dir': output_dir_full, 'plot_dir': plot_dir,
                'channel': 'All', 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    file_syst = template_outfilename.substitute(asimov=Asi, channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov=Asi, channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    if SignalInject:
        ylabel = f'Full analysis\nSignal Injected\n{WC}={InjectValue:0.2f}'
    else:
        ylabel = 'Full analysis\nAsimov Dataset'
    root_file_dict_full[N+1] = {'root_file_dict': root_file_dict, 'ylabel': ylabel,
                                   'variable_of_choice': ''}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    if SignalInject:
        plotfile = os.path.join(plot_dir, f'signal_inject_{WC}_full_analysis_and_channels_NLL_vs_{WC}{stat_str}{ScanType}')
    else:
        plotfile = os.path.join(plot_dir, f'full_analysis_and_channels_NLL_vs_{WC}{stat_str}{ScanType}')
    #title = f'{CL*100:0.1f}\% CL Limits on '+WC_l+f' {scan_title}\nFull Combination and Channel Results'
    title = f'Limits on '+WC_l+f' {scan_title}\nFull Combination and Channel Results'
    if SignalInject:
        ncol = 3
        title_on = True
        if WC in dim6_ops:
            lT = r'$/\Lambda^2$'
            lS = r'[TeV$^{-2}$]'
        else:
            lT = r'$/\Lambda^2$'
            lS = r'[TeV$^{-4}$]'
        title = 'Signal Injection Test: ' + WC_l + lT + rf'$={{ {InjectValue:0.1f} }}$ ' + lS + '\n'
    else:
        if plot_stat_only:
            ncol = 3
        else:
            ncol = 2
        title_on = False
    fig, ax = make_limit_NLL_summary_plot(WC, root_file_dict_full, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile, sort_by_lim=True, ncol=ncol, legend=legend, title_on=title_on, SignalInject=SignalInject)
    return fig, ax


if __name__=='__main__':
    # FIX ME! make these command line args
    #WCs = WC_ALL
    #WCs = ['cW'] # testing
    # confidence level
    #CL_list = [0.95, CL_1sigma]
    #CL_list = [0.95]
    # which scan type?
    # freeze all but one
    ScanType = '_1D'
    # profile
    #ScanType = '_All'
    # SM expectation
    expect_signal = '1'
    # confidence level
    #CL = 0.95
    #CL = CL_1sigma
    # legend = False
    legend = True
    # list of stat on / stat off
    pstats = [False] # only make the plot without stat only
    #pstats = [True] # only make the plot that includes stat only
    # pstats = [True, False] # both
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--InjectSignal',
                        help='Plot the results of a signal injection test? "n" (default) / "y". If "y", must supply --WC and --InjectValue')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW", ...]')
    parser.add_argument('-v', '--InjectValue',
                        help='What value for the WC was used in the signal injection test? 0.0 (default), 1.0, ...')
    args = parser.parse_args()
    if args.InjectSignal is None:
        args.InjectSignal = 'n'
    SignalInject = args.InjectSignal == 'y'
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs = WC_ALL + ['sm']
        #WCs = WC_ALL
    else:
        WCs = [args.WC]
    if args.InjectValue is None:
        InjectValue = 0.0
    else:
        InjectValue = float(args.InjectValue)
    # loop over WCs
    for WC in WCs:
        #if WC == 'sm':
        if (WC == 'sm') or SignalInject:
            CL_list = [CL_1sigma]
        else:
            CL_list = [0.95]
        print(f'WC: '+WC)
        # full analysis plot
        print("=========================================================")
        print("Making NLL plot with full combination and channel results...")
        for pstat in pstats:
            print(f'Include stat-only? {pstat}')
            run_NLL_plot_analysis_channel(WC, datacard_dict, CL_list, pstat,
                                          SignalInject=SignalInject, InjectValue=InjectValue,
                                          ScanType=ScanType, expect_signal=expect_signal,
                                          legend=legend)
        print("=========================================================\n")
    # plt.show()

