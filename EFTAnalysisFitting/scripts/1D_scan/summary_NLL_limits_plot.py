# same as NLL_limits_plot_from_dir.py, but adds full likelihood & channel breakdown
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
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
    WC_pretty_print_dict,
)
#from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting import config_plots, ticks_in, ticks_sizes, CMSify_title

config_plots()


colors_list = ['black', 'red', 'green', 'blue', 'purple', 'orange']

def make_limit_NLL_summary_plot(WC, root_file_dict_full, title, CL=0.95, plot_stat_only=False, savefile=None, sort_by_lim=True, ncol=2):
    # plot
    if ncol <= 2:
        fig = plt.figure(figsize=(16, 8))
        #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
        ax = fig.add_axes([0.05, 0.1, 0.50, 0.75])
    else:
        fig = plt.figure(figsize=(18, 8))
        ax = fig.add_axes([0.05, 0.1, 0.45, 0.75])
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
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
            Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC)
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
                    lw = 2.
                else:
                    lw = 1.
                label_NLL = info_dict['ylabel']+f'\n'
                # label_NLL += f'[{LLs[0]:0.3f}, {ULs[0]:0.3f}]\n'
                # multi interval
                label_NLL += '\n'.join([f'[{LL:0.3f}, {UL:0.3f}]' for LL, UL in zip(LLs[0], ULs[0])]) + '\n'
                ax.plot(Cs, NLL, c=colors_list[i], linestyle='-', linewidth=lw, label=label_NLL)
                if plot_stat_only:
                    Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, LLs_stat, ULs_stat = get_lims(CL_list, Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC)
                    #label_NLL = f'[{LLs_stat[0]:0.3f}, {ULs_stat[0]:0.3f}]\n(stat. only)\n'
                    # multi interval
                    label_NLL = '\n'.join([f'[{LL:0.3f}, {UL:0.3f}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])]) + '\n(stat. only)\n'
                    ax.plot(Cs_stat, NLL_stat, c=colors_list[i], linestyle='-.', linewidth=lw, label=label_NLL)
                # track limits for the x limits later
                LLs_all.append(LLs[0])
                ULs_all.append(ULs[0])
                # ylims
                ymax_min = min(np.max(NLL), ymax_min)
    # plot the horizontal line for NLL_cut only once at the end
    xmin = np.min(Cs)
    xmax = np.max(Cs)
    NLL_cut = NLL_cuts[0]
    #label = WC_l+f'@{CL*100:0.1f}\% CL'
    label = r'$\Delta$NLL Threshold' + f'\n{int(CL*100):d}\% CL'
    ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
    # axis labels
    if WC in dim6_ops:
        suff = r'$ / \Lambda^2$ [TeV]$^{-2}$'
    else:
        suff = r'$ / \Lambda^4$ [TeV]$^{-4}$'
    ax.set_xlabel(WC_l+suff, fontweight ='bold', loc='right', fontsize=20.)
    ax.set_ylabel(r'$\Delta$NLL', fontweight='bold', loc='top', fontsize=20.)
    ax.set_title(title+'\n', pad=3.)
    # ticks
    ax = ticks_in(ax)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax = ticks_sizes(ax, major={'L':15,'W':1.5}, minor={'L':8,'W':1})
    # set xlim to be symmetric
    # LLs_all = np.array(LLs_all)
    # ULs_all = np.array(ULs_all)
    xlim_factor = 2.
    xlim = xlim_factor*np.max(np.abs(np.concatenate([np.concatenate([LL for LL in LLs_all]), np.concatenate([UL for UL in ULs_all])])))
    ax.set_xlim([-xlim, xlim])
    #ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    if ymax_min > 2.5*np.max(NLL_cuts):
        yu = 2.5 * np.max(NLL_cuts)
    else:
        yu = ymax_min
    ax.set_ylim([-0.01, yu])
    ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=ncol)
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax

def run_NLL_plot_analysis_channel(WC, datacard_dict, CL, plot_stat_only, SignalInject=False, InjectValue=0.0, ScanType='_1D'):
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
    WC_l = WC_pretty_print_dict[WC]
    output_dir_ch = os.path.join(datacard_dir, 'output', 'channel')
    output_dir_full = os.path.join(datacard_dir, 'output', 'full_analysis')
    plot_dir = os.path.join(datacard_dir, 'plots', 'full_analysis', scan_dir)
    root_file_dict_full = {}
    # construct root file for each channel
    for i, ch in enumerate(sorted(datacard_dict.keys())):
        WCs = versions_dict[ch]['EFT_ops']
        if not WC in WCs:
            continue
        fname_ch = datacard_dict[ch]['info']['file_name']
        sname_ch = datacard_dict[ch]['info']['short_name']
        v = versions_dict[ch]['v']
        version = f'v{v}'
        bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                    'channel': fname_ch, 'subchannel': 'All',
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
    title = f'{CL*100:0.1f}\% CL Limits on '+WC_l+f' {scan_title}\nFull Combination and Channel Results'
    if SignalInject:
        ncol = 3
    else:
        ncol = 2
    fig, ax = make_limit_NLL_summary_plot(WC, root_file_dict_full, title, CL=CL, plot_stat_only=plot_stat_only, savefile=plotfile, sort_by_lim=True, ncol=ncol)
    return fig, ax


if __name__=='__main__':
    # FIX ME! make these command line args
    #WCs = ['cW'] # testing
    #WCs = ['cHB'] # testing
    #WCs = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1']
    WCs = WC_ALL
    # Asimov
    SignalInject=False
    InjectValue = 0.0
    # SignalInjection cW
    # SignalInject=True
    # InjectValue = 0.2
    # WCs = ['cW']
    # which scan type?
    # freeze all but one
    ScanType = '_1D'
    # profile
    #ScanType = '_All'
    # confidence level
    CL = 0.95
    for WC in WCs:
        print(f'WC: '+WC)
        # full analysis plot
        print("=========================================================")
        print("Making NLL plot with full combination and channel results...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            run_NLL_plot_analysis_channel(WC, datacard_dict, CL, pstat, SignalInject=SignalInject, InjectValue=InjectValue, ScanType=ScanType)
        print("=========================================================\n")
    # plt.show()

