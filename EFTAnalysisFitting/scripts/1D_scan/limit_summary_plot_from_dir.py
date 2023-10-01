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
    WC_pretty_print_dict,
)
# from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting import config_plots, ticks_in, ticks_sizes, CMSify_title

config_plots()

# this is a duplicate from limit_summary_plot.py
# could consider importing this function
def make_limit_summary_plot(WC, root_file_dict_full, title, CL=0.95, add_hrule=True, plot_stat_only=True,
                            xlim_factor=2.0, fixed_xlim=None, savefile=None, sort_by_lim=True,
                            plot_var_of_choice=True):
    # bottom to top, plots 0, 1, 2, 3, ....
    # plot
    if plot_var_of_choice:
        fig = plt.figure(figsize=(16, 8))
        ax = fig.add_axes([0.15, 0.1, 0.55, 0.8])
    # TEST BELOW
    else:
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_axes([0.15, 0.1, 0.75, 0.8])
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    # loop through files to plot
    LLs_all = []
    ULs_all = []
    yvals_all = []
    ylabels_all = []
    text_annot_all = []
    var_annot_all = []
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
            #Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC)
            hold = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
            Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
            # for multi lim version need to ensure single limit
            LLs = [np.min(LL) for LL in LLs]
            ULs = [np.max(UL) for UL in ULs]
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
            #Cs, NLL, CL_list, NLL_cuts, LLs, ULs, C_best_stat, NLL_best = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC)
            hold = get_lims_w_best([CL], Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
            #Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, _, _, LLs_stat, ULs_stat, C_best_stat, NLL_best_stat = hold
            Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
            # for multi lim version need to ensure single limit
            #LLs_stat = [np.min(LL) for LL in LLs_stat]
            #ULs_stat = [np.max(UL) for UL in ULs_stat]
            LLs = [np.min(LL) for LL in LLs]
            ULs = [np.max(UL) for UL in ULs]
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

def run_plot_subchannel(WC, channel, subchannel, datacard_dict, CL, ScanType, plot_stat_only, xlim_factor, fixed_xlim):
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    output_dir_bin = os.path.join(datacard_dir, 'output', 'single_bin')
    output_dir_sch = os.path.join(datacard_dir, 'output', 'subchannel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'subchannel', scan_dir)
    root_file_dict_full = {}
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
    # construct root file for each subchannel
    bins = datacard_dict[channel]['subchannels'][subchannel]['bins']
    for i, bin_ in enumerate(bins):
        bin_info = {'output_dir': output_dir_bin, 'plot_dir': plot_dir,
                    'channel': fname_ch, 'subchannel': fname_sch,
                    'version': version, 'bin_': bin_,
                    }
        sname_sch_b = sname_sch + f'_bin{bin_}'
        file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType,version=version, syst='syst', method='MultiDimFit')
        file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType,version=version, syst='nosyst', method='MultiDimFit')
        root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
        root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
        root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
        root_file_dict_full[i] = {'root_file_dict': root_file_dict, 'ylabel': f'{bin_}',
                                  'variable_of_choice': ''}
                                  # 'variable_of_choice': datacard_dict[channel]['info']['variable_of_choice']}
    # construct root file for subchannel (combined)
    N = len(bins)-1
    bin_info = {'output_dir': output_dir_sch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': 'All',
                }
    # FIXME! 'Asimov' should be passed in. Need to be able to run with data_obs, e.g. signal injection tests.
    file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType,version=version, syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType,version=version, syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    root_file_dict_full[N+1.25] = {'root_file_dict': root_file_dict, 'ylabel': 'combined',
                                   'variable_of_choice': datacard_dict[channel]['info']['variable_of_choice']}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'sensitivity_summary_channel-{channel}_subchannel-{subchannel}{stat_str}_{WC}{ScanType}')
    WC_lab = WC_pretty_print_dict[WC]
    title = f'{int(CL*100)}\% CL Sensitivity to '+WC_lab+f' {scan_title}: {channel}'
    if subchannel != '':
        title += f', {subchannel}'
    fig, ax = make_limit_summary_plot(WC, root_file_dict_full, title, CL=CL, add_hrule=True, plot_stat_only=plot_stat_only,
                                      xlim_factor=xlim_factor, fixed_xlim=fixed_xlim, savefile=plotfile)
    return fig, ax

def run_plot_channel(WC, channel, datacard_dict, CL, ScanType, plot_stat_only, xlim_factor, fixed_xlim):
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    output_dir_sch = os.path.join(datacard_dir, 'output', 'subchannel')
    output_dir_ch = os.path.join(datacard_dir, 'output', 'channel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'channel', scan_dir)
    root_file_dict_full = {}
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    # version number
    v = versions_dict[channel]['v']
    version = f'v{v}'
    # construct root file for each subchannel
    for i, subch in enumerate(sorted(datacard_dict[channel]['subchannels'].keys())):
        dc_subch = datacard_dict[channel]['subchannels'][subch]
        fname_sch = dc_subch['info']['file_name']
        sname_sch = dc_subch['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        bin_info = {'output_dir': output_dir_sch, 'plot_dir': plot_dir,
                    'channel': fname_ch, 'subchannel': subch,
                    'version': version, 'bin_': 'All',
                    }
        # FIXME! 'Asimov' should be passed in. Need to be able to run with data_obs, e.g. signal injection tests.
        file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType,version=version, syst='syst', method='MultiDimFit')
        file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType,version=version, syst='nosyst', method='MultiDimFit')
        root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
        root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
        root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
        root_file_dict_full[i] = {'root_file_dict': root_file_dict, 'ylabel': dc_subch['info']['ylabel_name'],
                                  'variable_of_choice': datacard_dict[channel]['info']['variable_of_choice']}
    # construct root file for channel (combined)
    N = len(datacard_dict[channel]['subchannels'].keys())-1
    bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    root_file_dict_full[N+1.25] = {'root_file_dict': root_file_dict, 'ylabel': 'combined',
                                   'variable_of_choice': datacard_dict[channel]['info']['variable_of_choice']}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'sensitivity_summary_channel-{channel}{stat_str}_{WC}{ScanType}')
    WC_lab = WC_pretty_print_dict[WC]
    title = f'{int(CL*100)}\% CL Sensitivity to '+WC_lab+f' {scan_title}: {channel}'
    fig, ax = make_limit_summary_plot(WC, root_file_dict_full, title, CL=CL, add_hrule=True, plot_stat_only=plot_stat_only,
                                      xlim_factor=xlim_factor, fixed_xlim=fixed_xlim, savefile=plotfile)
    return fig, ax

def run_plot_analysis(WC, datacard_dict, CL, ScanType, plot_stat_only, xlim_factor, fixed_xlim):
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    # output_dir_sch = os.path.join(datacard_dir, 'output', 'combined_datacards', 'subchannel')
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
        # FIXME! 'Asimov' should be passed in. Need to be able to run with data_obs, e.g. signal injection tests.
        file_syst = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
        file_stat = template_outfilename.substitute(asimov='Asimov', channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
        root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
        root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
        root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
        root_file_dict_full[i] = {'root_file_dict': root_file_dict, 'ylabel': datacard_dict[ch]['info']['ylabel_name'],
                                  'variable_of_choice': datacard_dict[ch]['info']['variable_of_choice']}
    # construct root file for full analysis
    N = len(datacard_dict.keys())-1
    version = 'vCONFIG_VERSIONS'
    bin_info = {'output_dir': output_dir_full, 'plot_dir': plot_dir,
                'channel': 'All', 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    file_syst = template_outfilename.substitute(asimov='Asimov', channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='syst', method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov='Asimov', channel='all', subchannel='_combined', WC=WC, ScanType=ScanType,version=version,syst='nosyst', method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    root_file_dict_full[N+1.25] = {'root_file_dict': root_file_dict, 'ylabel': 'combined',
                                   'variable_of_choice': ''}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'sensitivity_summary_all-channels{stat_str}_{WC}{ScanType}')
    # title = f'{int(CL*100)}% CL Sensitivity: All Channels'
    WC_lab = WC_pretty_print_dict[WC]
    title = f'{int(CL*100)}\% CL Sensitivity to '+WC_lab+f' {scan_title}'
    fig, ax = make_limit_summary_plot(WC, root_file_dict_full, title, CL=CL, add_hrule=True, plot_stat_only=plot_stat_only,
                                      xlim_factor=xlim_factor, fixed_xlim=fixed_xlim, savefile=plotfile)
    return fig, ax


if __name__=='__main__':
    # FIXME! make these cmd line args
    #WC = 'cW'
    CL = 0.95
    # which scan type?
    # freeze all but one
    ScanType = '_1D'
    # profile
    #ScanType = '_All'
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW", ...]')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WC_ALL
    else:
        WCs_loop = [args.WC]
    # VERSION = 'v1'
    #########################
    # outer loop (over WC)
    for WC in WCs_loop:
    # for WC in ['cW']: # testing
        print(f'WC: '+WC)
        # loop through all subchannels and plot
        print("=========================================================")
        print("Making sensitivity plots for each subchannel...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            for ch in datacard_dict.keys():
                WCs = versions_dict[ch]['EFT_ops']
                if not WC in WCs:
                    continue
                print(ch)
                for sch in datacard_dict[ch]['subchannels'].keys():
                    print(sch)
                    fig, ax = run_plot_subchannel(WC, ch, sch, datacard_dict, CL=CL, ScanType=ScanType, plot_stat_only=pstat, xlim_factor=2.0, fixed_xlim=None)
                    # fig, ax = run_plot_subchannel(ch, sch, datacard_dict, version=VERSION, CL=CL, plot_stat_only=pstat, xlim_factor=None, fixed_xlim=[-2., 2.])
        print("=========================================================\n")
        # loop through all channels and plot
        print("=========================================================")
        print("Making sensitivity plots for each channel...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            for ch in datacard_dict.keys():
                WCs = versions_dict[ch]['EFT_ops']
                if not WC in WCs:
                    continue
                print(ch)
                fig, ax = run_plot_channel(WC, ch, datacard_dict, CL=CL, ScanType=ScanType, plot_stat_only=pstat, xlim_factor=1.2, fixed_xlim=None)
                # fig, ax = run_plot_channel(ch, datacard_dict, version=VERSION, CL=CL, plot_stat_only=pstat, xlim_factor=None, fixed_xlim=[-2., 2.])
        print("=========================================================\n")
        #####
        print("=========================================================")
        print("Making sensitivity plots for full analysis...")
        for pstat in [True, False]:
            print(f'Include stat-only? {pstat}')
            fig, ax = run_plot_analysis(WC, datacard_dict, CL=CL, ScanType=ScanType, plot_stat_only=pstat, xlim_factor=1.2, fixed_xlim=None)
            # fig, ax = run_plot_analysis(WC, datacard_dict, CL=CL, plot_stat_only=pstat, xlim_factor=None, fixed_xlim=[-0.5., 0.5])
        print("=========================================================\n")

        # plt.show()
