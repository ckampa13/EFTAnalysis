# same as NLL_limits_plot_from_dir.py, but adds full likelihood & channel breakdown
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
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
from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting import config_plots, ticks_in, ticks_sizes, CMSify_title

config_plots()

#########
# REFERENCE ONLY !! (for adding multiple curves from root_file_dict)
def make_limit_summary_plot(WC, root_file_dict_full, title, CL=0.95, add_hrule=True, plot_stat_only=True, xlim_factor=2.0, fixed_xlim=None, savefile=None, sort_by_lim=True,
                            plot_var_of_choice=True):
    # bottom to top, plots 0, 1, 2, 3, ....

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
                label_total = r'Proj. (stat. $\bigoplus$ syst.)'+'\nAsimov Dataset'
                label_stat = 'stat. only'
            else:
                label_total = None
                label_stat = None
            yval, info_dict = item
            if loop == 1:
                yvals_all.append(yval)
            root_file_dict = info_dict['root_file_dict']
            if loop == 1:
                ylabels_all.append(info_dict['ylabel'])
            var_of_choice = info_dict['variable_of_choice']
            # get limits and plot
            # total
            Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC)
            err_low = C_best - LLs[0]
            err_high = ULs[0] - C_best
            #err_mean = (err_low + err_high) / 2.
            # use width of the limit
            err_mean = (ULs[0] - LLs[0])
            if loop == 0:
                errs_list.append(err_mean)
                ys_start_list.append(yval)
            if loop == 1:
                ax.errorbar([C_best], [yval], xerr=[[err_low],[err_high]], c='black', capsize=8.0, linestyle='-', linewidth=2, capthick=2, markersize=16, marker='.', zorder=8, label=label_total)
                LLs_all.append(LLs[0])
                ULs_all.append(ULs[0])
            if abs(np.round(C_best, 3)) < 0.001:
                best_str = f'{0.0:0.3f}'
            else:
                best_str = f'{C_best:0.3f}'
            #text_annot = rf'   ${best_str}\ ~^{{+ {err_high:0.3f} }}_{{- {err_low:0.3f} }}$'
            text_annot = rf'${best_str}\ ~^{{+ {err_high:0.3f} }}_{{- {err_low:0.3f} }}$'
            # stat only
            # add to label either way
            Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best_stat, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC)
            err_low = C_best - LLs[0]
            err_high = ULs[0] - C_best
            text_annot += rf'$\ ~^{{+ {err_high:0.3f} }}_{{- {err_low:0.3f} }}$'
            if plot_stat_only:
                # ax.errorbar([FT0_best], [yval], xerr=[[err_low],[err_high]], c='blue', capsize=0., linestyle='-', linewidth=6, zorder=7, label=label_stat)
                if loop == 1:
                    ax.errorbar([C_best], [yval], xerr=[[err_low],[err_high]], c='magenta', capsize=0., linestyle='-', linewidth=6, zorder=7, label=label_stat)
            if loop == 1:
                text_annot_all.append(text_annot)
                #var_annot_all.append(rf'                                       {var_of_choice}')
                #var_annot_all.append(r'$\textcolor{white}{|}\qquad \qquad \qquad \qquad \qquad$'+var_of_choice)
                var_annot_all.append(var_of_choice)
    # axis labels
    if WC in dim6_ops:
        suff = r'$ / \Lambda^2$ [TeV]$^{-2}$'
    else:
        suff = r'$ / \Lambda^4$ [TeV]$^{-4}$'
    WC_lab = WC_pretty_print_dict[WC]
    ax.set_xlabel('Sensitivity to '+WC_lab+suff)
    ax.set_title(title+'\n', pad=3.)
    # set xlim to be symmetric
    LLs_all = np.array(LLs_all)
    ULs_all = np.array(ULs_all)
    if xlim_factor is None:
        ax.set_xlim(fixed_xlim)
        # xlim = np.max(np.abs(fixed_xlim))
        xlim = np.min(np.abs(fixed_xlim))
    else:
        xlim = xlim_factor*np.max(np.abs([LLs_all, ULs_all]))
        ax.set_xlim([-xlim, xlim])
    # add dummy point above top for label space and below for aesthetics
    yvals = sorted(root_file_dict_full.keys())
    yrange = np.max(yvals) - np.min(yvals)
    ax.scatter([0.], [np.max(yvals) + 0.30 * yrange], s=0., alpha=0.)
    ax.scatter([0.], [np.min(yvals) - 0.1 * yrange], s=0., alpha=0.)
    # add rule between combined and others
    # additional annotations
    # total, stat
    #header_str = '               total   stat.'
    header_str = r'total$\ \ \ \ $stat.'
    # if plot_stat_only:
    #     header_str = '               total   stat.'
    # else:
    #     header_str = '               total'
    header_y = np.min([np.max(yvals) + 0.5, np.max(yvals) + 0.30 * yrange])
    ax.annotate(header_str, (1.00*xlim, header_y), (1.22*xlim, header_y), xycoords='data')
    # var of choice header
    # var_header_str = ('                                       Variable of\n'+
    #                   '                                       choice')
    # var_header_str = (r'$\textcolor{green}{~}\qquad \qquad \qquad \qquad \qquad$'+'Variable of\n'+r'$\textcolor{white}{~}\qquad \qquad \qquad \qquad \qquad$'+'choice')
    if plot_var_of_choice:
        var_header_str = 'Variable of\nchoice'
        ax.annotate(var_header_str, (1.00*xlim, header_y),  (1.65*xlim, header_y), xycoords='data')
    # formatting
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax = ticks_in(ax)
    ax = ticks_sizes(ax, major={'L':10,'W':1.1}, minor={'L':4,'W':0.8})
    ax.set_yticks(yvals)
    ax.set_yticklabels(ylabels_all)
    # only want vertical grid lines
    ax.grid(axis='y')
    # ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    ax.legend(loc='upper left')
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax

############

def make_limit_NLL_summary_plot(WC, root_file_dict_full, title, CL=0.95, plot_stat_only=False, savefile=None, sort_by_lim=True):
    # plot
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    WC_l = WC_pretty_print_dict[WC]
    # loop through files to plot
    LLs_all = []
    ULs_all = []
    yvals_all = []
    ylabels_all = []
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






    # get limits and plot
    # total
    Cs, NLL, CL_list, NLL_cuts, LLs, ULs = get_lims(CL_list, Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC)
    ax.plot(Cs, NLL, c='blue', linestyle='-', linewidth=2, label='Expected\nAsimov Dataset')
    # stat only
    if plot_stat_only:
        Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, LLs_stat, ULs_stat = get_lims(CL_list, Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC)
        ax.plot(Cs_stat, NLL_stat, c='blue', linestyle='-.', linewidth=2, label='Expected (stat. only)')
    # loop through CLs to determine limits
    xmin = np.min(Cs)
    xmax = np.max(Cs)
    if plot_stat_only:
        for CL, NLL_cut, LL, UL, LL_s, UL_s in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat):
            # build label
            label = WC_l+f'@{CL*100:0.1f}%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
            # add to the plot
            ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
    else:
        for CL, NLL_cut, LL, UL, in zip(CL_list, NLL_cuts, LLs, ULs):
            # build label
            label = WC_l+f'@{CL*100:0.1f}%:\n[{LL:0.3f}, {UL:0.3f}]'
            # add to the plot
            ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
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
    # axis limits
    if plot_stat_only:
        largest_lim = 2*np.max(np.abs(np.array([LLs, ULs, LLs_stat, ULs_stat])))
    else:
        largest_lim = 2*np.max(np.abs(np.array([LLs, ULs])))
    xlim = np.max(np.abs([xmin, xmax]))
    xlim2 = np.min(np.abs([xmin, xmax]))
    if largest_lim < xlim:
        ax.set_xlim([-largest_lim, largest_lim])
    else:
        ax.set_xlim([-xlim2, xlim2])
    ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax

def run_lim_plot_bin(WC, channel, subchannel, bin_, datacard_dict, CL_list, plot_stat_only):
    WC_l = WC_pretty_print_dict[WC]
    output_dir_bin = os.path.join(datacard_dir, 'output', 'single_bin')
    plot_dir = os.path.join(datacard_dir, 'plots', 'single_bin')
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    # update subchannel name if there is rescaling
    if versions_dict[channel]['lumi'] == '2018':
        sname_sch += '_2018_scaled'
        print(' (2018 scaled)', end='')
    # version number
    v = versions_dict[channel]['v']
    version = f'v{v}'
    # plotting info
    bin_info = {'output_dir': output_dir_bin, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': bin_,
                }
    sname_sch_b = sname_sch + f'_bin{bin_}'
    # construct root file name
    # note version number not in single bin single channel output ROOT files. FIXME! Make this consistent.
    file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType='_1D',version=version, syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_{WC}_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}')
    title = 'Limits on '+WC_l+f'\nChannel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_subchannel(WC, channel, subchannel, datacard_dict, CL_list, plot_stat_only):
    WC_l = WC_pretty_print_dict[WC]
    output_dir_sch = os.path.join(datacard_dir, 'output', 'subchannel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'subchannel')
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    # update subchannel name if there is rescaling
    if versions_dict[channel]['lumi'] == '2018':
        sname_sch += '_2018_scaled'
        print(' (2018 scaled)', end='')
    # version number
    v = versions_dict[channel]['v']
    version = f'v{v}'
    bin_info = {'output_dir': output_dir_sch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType='_1D',version=version, syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_{WC}_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}')
    title = 'Limits on '+WC_l+f'\nChannel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_channel(WC, channel, datacard_dict, CL_list, plot_stat_only):
    WC_l = WC_pretty_print_dict[WC]
    output_dir_ch = os.path.join(datacard_dir, 'output', 'channel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'channel')
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    # version number
    v = versions_dict[channel]['v']
    version = f'v{v}'
    bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType='_1D',version=version,syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType='_1D',version=version,syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_{WC}_channel-{channel}_bin{bin_info["bin_"]}{stat_str}')
    title = 'Limits on '+WC_l+f'\nChannel: {bin_info["channel"]}, {bin_info["subchannel"]}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_analysis(WC, datacard_dict, CL_list, plot_stat_only, version=None):
    WC_l = WC_pretty_print_dict[WC]
    if version is None:
        version = 'vCONFIG_VERSIONS'
    output_dir_full = os.path.join(datacard_dir, 'output', 'full_analysis')
    plot_dir = os.path.join(datacard_dir, 'plots', 'full_analysis')
    # construct root file name
    file_syst = template_outfilename.substitute(asimov='Asimov', channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version=version, syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(output_dir_full, file_syst)
    root_file_stat = os.path.join(output_dir_full, file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': None}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_{WC}_channel-All_binAll{stat_str}')
    title = 'Limits on '+WC_l+f'\nChannel: All; Bin: All'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax


if __name__=='__main__':
    # FIX ME! make these command line args
    #WC = 'cW'
    WCs = WC_ALL
    # confidence level
    CL_list = [0.95, CL_1sigma]
    for WC in WCs:
    # for WC in ['cW']: # testing
        print(f'WC: '+WC)
        # loop through all bins and plot
        print("=========================================================")
        print("Making likelihood plots for each bin...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            for ch in datacard_dict.keys():
                if WC not in versions_dict[ch]['EFT_ops']:
                    continue
                print(f'Channel: {ch}')
                for sch in datacard_dict[ch]['subchannels'].keys():
                    print(f'{sch}: ', end='')
                    for bin_ in datacard_dict[ch]['subchannels'][sch]['bins']:
                        print(f'{bin_} ', end='')
                        fig, ax = run_lim_plot_bin(WC, ch, sch, bin_, datacard_dict, CL_list, plot_stat_only=pstat)
                    print()
        print("=========================================================\n")
        # loop through all subchannels and plot
        print("=========================================================")
        print("Making likelihood plots for each subchannel...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            for ch in datacard_dict.keys():
                if WC not in versions_dict[ch]['EFT_ops']:
                    continue
                print(f'Channel: {ch}')
                for sch in datacard_dict[ch]['subchannels'].keys():
                    print(sch)
                    fig, ax = run_lim_plot_subchannel(WC, ch, sch, datacard_dict, CL_list, plot_stat_only=pstat)
        print("=========================================================\n")
        # loop through all channels and plot
        print("=========================================================")
        print("Making likelihood plots for each channel...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            for ch in datacard_dict.keys():
                if WC not in versions_dict[ch]['EFT_ops']:
                    continue
                print(ch)
                fig, ax = run_lim_plot_channel(WC, ch, datacard_dict, CL_list, plot_stat_only=pstat)
        print("=========================================================\n")
        #####
        print("=========================================================")
        print("Making likelihood plots for full analysis...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            fig, ax = run_lim_plot_analysis(WC, datacard_dict, CL_list, plot_stat_only=pstat)
        print("=========================================================\n")
    # plt.show()

