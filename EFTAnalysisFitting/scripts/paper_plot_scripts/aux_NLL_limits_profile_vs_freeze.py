# this script mirrors NLL_limits_plot.py, but also plots the stat-only / nosyst likelihood as well.
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import argparse
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
import json

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, WCs_NDIM
from MISC_CONFIGS import (
    datacard_dir,
    #template_filename,
    template_outfilename,
    #template_outfilename_stub,
    dim6_ops,
    #WC_pretty_print_dict,
    WC_pretty_print_dict_AN,
    #SR_pretty_print_dict_AN,
)
WC_pretty_print_dict = WC_pretty_print_dict_AN
#SR_pretty_print_dict = SR_pretty_print_dict_AN
# from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title, numerical_formatter

config_plots(grid=True)
plt.rcParams['figure.constrained_layout.use'] = True

# FIXME! Is "ScanType" needed in this function?
def make_limit_plot(WC, root_file_dict, title, CL_list=[CL_1sigma, 0.95], savefile=None, legend=True, tight_layout=False, xlim_force=None, limits_legend=False):
    output_json = {'points': {}, 'legend': {}}
    # colors
    if 'Asimov' in root_file_dict['freeze']:
        c_prof = 'lime'
        c_freeze = 'blue'
    else:
        #c_prof = 'purple'
        c_prof = 'blue'
        c_freeze = 'magenta'
    # plot
    #fig = plt.figure(figsize=(16, 8))
    #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    fig, ax = plt.subplots()
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=False, inside_frame=False)
    WC_l = WC_pretty_print_dict[WC]
    # get limits and plot
    if 'prof' in root_file_dict.keys():
        # profile
        hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['prof'], WC=WC, extrapolate=True)
        # hold = get_lims(CL_list, Cs=None, NLL=None, root_file=root_file_dict['prof'], WC=WC, extrapolate=True)
        Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
        label = 'Profile Other WCs'
        if limits_legend:
            label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])])# + '\n'
            CL_ = f'{CL_list[0]*100:0.0f}'
            label += f' ({CL_}' + r'$\%$ CL)'
            output_json['legend'][f'{WC}_LL_95CL_profile'] = [float(numerical_formatter(LL)) for LL in LLs[0]]
            output_json['legend'][f'{WC}_UL_95CL_profile'] = [float(numerical_formatter(UL)) for UL in ULs[0]]
        ax.plot(Cs, 2.*NLL, c=c_prof, linestyle='-', linewidth=4, zorder=6, label=label)
        output_json['points']['x_vec_profile'] = Cs.tolist()
        output_json['points']['y_vec_profile'] = (2.*NLL).tolist()
    # freeze
    hold_f = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['freeze'], WC=WC, extrapolate=True)
    # hold_f = get_lims(CL_list, Cs=None, NLL=None, root_file=root_file_dict['freeze'], WC=WC, extrapolate=True)
    Cs_f, NLL_f, CL_list_f, NLL_cuts_f, _, _, LLs_f, ULs_f, C_best_f, NLL_best_f = hold_f
    label_f = 'Freeze Other WCs'
    if limits_legend:
        label_f += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_f[0], ULs_f[0])])# + '\n'
        CL_ = f'{CL_list_f[0]*100:0.0f}'
        label_f += f' ({CL_}' + r'$\%$ CL)'
        output_json['legend'][f'{WC}_LL_95CL_freeze'] = [float(numerical_formatter(LL)) for LL in LLs_f[0]]
        output_json['legend'][f'{WC}_UL_95CL_freeze'] = [float(numerical_formatter(UL)) for UL in ULs_f[0]]
    ax.plot(Cs_f, 2.*NLL_f, c=c_freeze, linestyle='-', linewidth=5, zorder=5, label=label_f)
    output_json['points']['x_vec_freeze'] = Cs_f.tolist()
    output_json['points']['y_vec_freeze'] = (2.*NLL_f).tolist()
    if 'prof' in root_file_dict.keys():
        # loop through CLs to determine limits
        xmin = np.min(Cs)
        xmax = np.max(Cs)
        # if plot_stat_only:
        largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs), np.concatenate(LLs_f), np.concatenate(ULs_f)]))))
    else:
        # loop through CLs to determine limits
        xmin = np.min(Cs_f)
        xmax = np.max(Cs_f)
        # if plot_stat_only:
        largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs_f), np.concatenate(ULs_f)]))))
    # else:
    #     largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs)]))))
    xlim = np.max(np.abs([xmin, xmax]))
    xlim2 = np.min(np.abs([xmin, xmax]))
    for CL, NLL_cut, ls in zip(CL_list, NLL_cuts_f, ['-', '--', '-.', ':',]):
        # build label
        #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
        # multi interval
        # label = WC_l+f'@{CL*100:0.1f}' + r'$\%$' + '\n'
        # label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n\n'
        # label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL_s, UL_s)]) + '\n(stat. only)\n'
        if CL > 0.9:
            #label = r'$2\Delta$NLL threshold'+f'\n{CL*100:0.0f}'+r'$\%$ CL'
            label = f'{CL*100:0.0f}'+r'$\%$ CL' + '\n threshold'
        else:
            # label = r'$2\Delta$NLL threshold'+f'\n{CL*100:0.1f}'+r'$\%$ CL'
            label = f'{CL*100:0.1f}'+r'$\%$ CL' + '\n threshold'
        # add to the plot
        #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
        #        linewidth=3,) #label=label)
        ax.plot([-2.*largest_lim, 2.*largest_lim],[2.*NLL_cut, 2.*NLL_cut], 'r', linestyle=ls,
               linewidth=3, label=label)
        output_json['points'][f'2DeltaNLL_{CL_list[0]*100:0.0f}CL'] = {'x_vec': [-2.*largest_lim, 2.*largest_lim], 'y_vec': 2*[2.*NLL_cut]}

    if WC in dim6_ops:
        suff = r'$ / \Lambda^2$ [TeV$^{-2}$]'
    else:
        suff = r'$ / \Lambda^4$ [TeV$^{-4}$]'
    ax.set_xlabel(WC_l+suff, fontweight ='bold', loc='right',)# fontsize=20.)
    ax.set_ylabel(r'$2\Delta$NLL', fontweight='bold', loc='top',)# fontsize=20.)
    ##ax.set_title(title+'\n', pad=3.)
    # ticks
    ax = ticks_in(ax)
    ax.xaxis.set_major_locator(MaxNLocator(7))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax = ticks_sizes(ax, major={'L':15,'W':1.5}, minor={'L':8,'W':1})
    # axis limits
    # if plot_stat_only:
    #     largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs), np.concatenate(LLs_stat), np.concatenate(ULs_stat)]))))
    # else:
    #     largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs)]))))
    # xlim = np.max(np.abs([xmin, xmax]))
    # xlim2 = np.min(np.abs([xmin, xmax]))
    if largest_lim < xlim:
        ax.set_xlim([-largest_lim, largest_lim])
    else:
        #ax.set_xlim([-xlim2, xlim2])
        ax.set_xlim([-largest_lim, largest_lim])
    ax.set_ylim([-0.01, 2.5*np.max(2*NLL_cuts_f)])
    # force xlim
    if not xlim_force is None:
        ax.set_xlim([-xlim_force, xlim_force])
    if legend:
        #ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        ax.legend(loc='upper center', framealpha=0.9, ncol=2, columnspacing=0.4, handlelength=1.0).set_zorder(9)
    #if tight_layout:
    #    fig.tight_layout()
    # DEBUG!!
    #ax.set_xlim([-1, 1])
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
        # json
        with open(savefile+'.json', 'w') as json_file:
            json.dump(output_json, json_file, indent=4)

    return fig, ax

def run_lim_plot_analysis(WC, datacard_dict, CL_list, version=None, legend=True, tight_layout=False, xlim_force=None, limits_legend=False, Asimov=True, Unblind=False):
    scan_dir = 'compare'
    FS_suff = ''
    WC_l = WC_pretty_print_dict[WC]
    if version is None:
        version = 'vCONFIG_VERSIONS'
    version_prof = version + '_NDIM'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_full = os.path.join(dcdir, 'output', 'full_analysis')
    plot_dir = os.path.join(dcdir, 'paper_plots', 'auxiliary', '')
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    # construct root file name
    file_prof = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType='_All',version=version_prof, syst='syst'+FS_suff, method='MultiDimFit')
    file_freeze = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version=version, syst='syst'+FS_suff, method='MultiDimFit')
    root_file_prof = os.path.join(output_dir_full, file_prof)
    root_file_freeze = os.path.join(output_dir_full, file_freeze)
    #root_file_dict = {'prof': root_file_prof, 'freeze': root_file_freeze, 'bin_info': None}
    # plot
    #if plot_stat_only:
    #    stat_str = '_w_stat_only'
    #else:
    #    stat_str = ''
    #plotfile = os.path.join(plot_dir, f'{asi_prestr}compare_profile_vs_freeze_NLL_vs_{WC}_channel-All_binAll_syst{vsuff}{FS_suff}')
    if WC in dim6_ops:
        root_file_dict = {'prof': root_file_prof, 'freeze': root_file_freeze, 'bin_info': None}
        plotfile = os.path.join(plot_dir + f'fig_NLL_vs_{WC}_profile_vs_freeze_{asi_output}')
    else:
        root_file_dict = {'freeze': root_file_freeze, 'bin_info': None}
        plotfile = os.path.join(plot_dir + f'fig_NLL_vs_{WC}_freeze_{asi_output}')
    #title = 'Limits on '+WC_l+f' {scan_title}\nChannel: All; Bin: All'
    title = 'Limits on '+WC_l+f'\nChannel: All; Bin: All'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend)
    return fig, ax


if __name__=='__main__':
    WCs_aux = ['cW', 'cHq3', 'cHq1', 'FT0', 'FT1', 'FT3']
    # FIX ME! make these command line args
    Asimov=False
    Unblind=True
    generate_full = True
    # confidence level
    #CL_list = [0.95, CL_1sigma]
    CL_list = [0.95]
    legend = True
    tight_layout=True
    # list of stat on / stat off
    pstats = [False] # only make the plot that includes syst only
    # pstats = [True, False] # both
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default), "all_aux",...]')
    # parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    # parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    # parser.add_argument('-v', '--VersionSuff',
    #                     help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    parser.add_argument('-x', '--xlim_force',
                        help='Override any algorithms internally deciding xlims for the plots. ["" (default, use algorithms), "0.5", "0.1", ...]')
    parser.add_argument('-l', '--LimitsLegend',
                        help='Add 95% CL limits to the legend? ["y" (default), "n"]')
    args = parser.parse_args()

    if args.WC is None:
        args.WC = ['cW']
    else:
        if args.WC == 'all_aux':
            WCs = WCs_aux
        else:
            WCs = [args.WC]
    ###
    # if args.VersionSuff is None:
    #     vsuff = ''
    # else:
    #     vsuff = args.VersionSuff
    if args.xlim_force is None:
        xlim_force = None
    else:
        xlim_force = float(args.xlim_force)
    if args.LimitsLegend is None:
        limits_legend = True
    else:
        limits_legend = args.LimitsLegend == 'y'
    # loop
    for WC in WCs:
    # for WC in ['cW']: # testing
        print(f'WC: '+WC)
        if generate_full:
            #####
            print("=========================================================")
            print("Making likelihood plots for full analysis...")
            for pstat in pstats:
                print(f'Include stat-only? {pstat}')
                fig, ax = run_lim_plot_analysis(WC, datacard_dict, CL_list, legend=legend, tight_layout=tight_layout,
                                                xlim_force=xlim_force, limits_legend=limits_legend,
                                                Asimov=Asimov, Unblind=Unblind)
            print("=========================================================\n")
    # plt.show()

