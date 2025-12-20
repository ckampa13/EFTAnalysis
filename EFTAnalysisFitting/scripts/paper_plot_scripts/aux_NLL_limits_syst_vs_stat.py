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
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, WCs_NDIM
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
def make_limit_plot(WC, root_file_dict, title, CL_list=[CL_1sigma, 0.95], ScanType='_1D', plot_stat_only=True, savefile=None, legend=True, tight_layout=False, xlim_force=None, limits_legend=False, Asimov=True):
    output_json = {'points': {}, 'legend': {}}
    if Asimov:
        c_stat = 'black'
        c_syst = 'blue'
    else:
        #c_stat = 'darkgreen'
        c_stat = 'black'
        c_syst = 'magenta'
        # c_syst = 'red'
    # plot
    #fig = plt.figure(figsize=(16, 8))
    #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    fig, ax = plt.subplots()
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=False, inside_frame=False)
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    # get limits and plot
    # total
    hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
    Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
    label = 'With systematics'
    if limits_legend:
        #label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])])# + '\n'
        CL = CL_list[0]
        label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])]) + f' ({CL*100:0.0f}' + r'$\%$ CL)'
        output_json['legend'][f'{WC}_LL_95CL_syst'] = [float(numerical_formatter(LL)) for LL in LLs[0]]
        output_json['legend'][f'{WC}_UL_95CL_syst'] = [float(numerical_formatter(UL)) for UL in ULs[0]]
    ax.plot(Cs, 2.*NLL, c=c_syst, linestyle='-', linewidth=4, zorder=5, label=label)# label='Expected\nAsimov Dataset')
    output_json['points']['x_vec_syst'] = Cs.tolist()
    output_json['points']['y_vec_syst'] = (2.*NLL).tolist()

    # stat only
    if plot_stat_only:
        hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
        Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, _, _, LLs_stat, ULs_stat, C_best_stat, NLL_best_stat = hold
        #label='Statistical Uncertainties\nOnly'
        label='Statistical\nuncertainties only'
        if limits_legend:
            #label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])])# + '\n'
            CL = CL_list[0]
            label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])]) + f' ({CL*100:0.0f}' + r'$\%$ CL)'
            output_json['legend'][f'{WC}_LL_95CL_stat'] = [float(numerical_formatter(LL)) for LL in LLs_stat[0]]
            output_json['legend'][f'{WC}_UL_95CL_stat'] = [float(numerical_formatter(UL)) for UL in ULs_stat[0]]
        ax.plot(Cs_stat, 2.*NLL_stat, c=c_stat, linestyle=':', linewidth=4, zorder=6, label=label)#label='Expected (stat. only)')
        output_json['points']['x_vec_stat'] = Cs_stat.tolist()
        output_json['points']['y_vec_stat'] = (2.*NLL_stat).tolist()
    # loop through CLs to determine limits
    xmin = np.min(Cs)
    xmax = np.max(Cs)
    if plot_stat_only:
        largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs), np.concatenate(LLs_stat), np.concatenate(ULs_stat)]))))
    else:
        largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs)]))))
    xlim = np.max(np.abs([xmin, xmax]))
    xlim2 = np.min(np.abs([xmin, xmax]))
    if plot_stat_only:
        #for CL, NLL_cut, LL, UL, LL_s, UL_s, ls in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat, ['--', '-.', ':',]):
        for CL, NLL_cut, LL, UL, LL_s, UL_s, ls in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat, ['-', '--', '-.', ':',]):
            # build label
            #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
            # multi interval
            #label = WC_l+f'@{CL*100:0.1f}%:\n'
            #label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n\n'
            #label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL_s, UL_s)]) + '\n(stat. only)\n'
            if CL > 0.9:
                #label = r'$2\Delta$NLL threshold'+f'\n{CL*100:0.0f}'+r'$\%$ CL'
                label = f'{CL*100:0.0f}'+r'$\%$ CL' + '\n threshold'
            else:
                # label = r'$2\Delta$NLL threshold'+f'\n{CL*100:0.1f}'+r'$\%$ CL'
                label = f'{CL*100:0.1f}'+r'$\%$ CL' + '\n threshold'
            # add to the plot
            #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
            #        linewidth=3,) #label=label)
            lc = 'red'
            # lc = 'gray'
            ax.plot([-2.*largest_lim, 2.*largest_lim], [2.*NLL_cut, 2.*NLL_cut], color=lc, linestyle=ls,
                   linewidth=3, label=label, zorder=100)
            output_json['points'][f'2DeltaNLL_{CL_list[0]*100:0.0f}CL'] = {'x_vec': [-2.*largest_lim, 2.*largest_lim], 'y_vec': 2*[2.*NLL_cut]}
    else:
        for CL, NLL_cut, LL, UL, ls in zip(CL_list, NLL_cuts, LLs, ULs, ['--', '-.', ':',]):
            # build label
            #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]'
            # multi interval
            label = WC_l+f'@{CL*100:0.1f}%:\n'
            label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n'
            # add to the plot
            #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
            #        linewidth=3,) #label=label)
            ax.plot([-2.*largest_lim, 2.*largest_lim], [2.*NLL_cut, 2.*NLL_cut], 'r', linestyle=ls,
                   linewidth=3, zorder=100) #label=label)
            output_json['points'][f'2DeltaNLL_{CL_list[0]*100:0.0f}CL'] = {'x_vec': [-2.*largest_lim, 2.*largest_lim], 'y_vec': 2*[2.*NLL_cut]}
    if WC == 'sm':
        suff = r' ($\mu_{\mathrm{SM}}$)'
    else:
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
    #ax.xaxis.set_major_locator(MaxNLocator(6))
    # ax.xaxis.set_major_locator(MaxNLocator(8))
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
    ###ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    ax.set_ylim([-0.25, 2.5*np.max(2*NLL_cuts)])
    ###ax.set_ylim([-0.25, 4.*np.max(2*NLL_cuts)])
    # force xlim
    if not xlim_force is None:
        ax.set_xlim([-xlim_force, xlim_force])
    if legend:
        #ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        ##ax.legend(loc='upper left', framealpha=1.0).set_zorder(9)
        ax.legend(loc='upper center', frameon=True, framealpha=0.9, ncol=2, columnspacing=0.4, handlelength=1.0).set_zorder(9)
    #if tight_layout:
    #    fig.tight_layout()
    # DEBUG!!
    #ax.set_xlim([-1, 1])
    # DEBUG!!
    #ax.set_ylim([0.000, 0.03])
    ##ax.set_ylim([0.000, 50.0])
    #ax.set_ylim([0.000, 1.0])
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
        # json
        with open(savefile+'.json', 'w') as json_file:
            json.dump(output_json, json_file, indent=4)

    return fig, ax

def run_lim_plot_analysis(WC, datacard_dict, CL_list, ScanType, plot_stat_only, version=None, legend=True, tight_layout=False, vsuff='', xlim_force=None, limits_legend=False, psuff='', Asimov=True, Unblind=False):
    LinO_str = ''
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    if WC == 'sm':
        ST = ''
    else:
        ST = ScanType+LinO_str
    FS_suff = ''
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    if version is None:
        version = 'vCONFIG_VERSIONS'
    version += vsuff
    dir_ = 'full_analysis'
    suff_sc = ''
    suff_ch_file = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_full = os.path.join(dcdir, 'output', dir_)
    plot_dir = os.path.join(dcdir, 'paper_plots', 'auxiliary')
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    if WC == 'sm':
        asi_output += '_expect_signal_1'
    # construct root file name
    file_syst = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined'+suff_sc, WC=WC, ScanType=ST,version=version, syst='syst'+FS_suff, method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined'+suff_sc, WC=WC, ScanType=ST,version=version, syst='nosyst'+FS_suff, method='MultiDimFit')
    root_file_syst = os.path.join(output_dir_full, file_syst)
    root_file_stat = os.path.join(output_dir_full, file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': None}
    # plot
    pfilename = f'fig_NLL_vs_{WC}_{scan_dir}_{asi_output}_syst_vs_statonly'
    plotfile = os.path.join(plot_dir, pfilename)
    title = 'Limits on '+WC_l+f' {scan_title}\nChannel: All; Bin: All'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, ScanType=ScanType, plot_stat_only=plot_stat_only, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend, Asimov=Asimov)
    return fig, ax


if __name__=='__main__':
    # FIX ME! make these command line args
    Unblind=True
    Asimov=False
    generate_full = True
    CL_list = [0.95]
    # which scan type?
    ScanType = '_1D'
    legend = True
    tight_layout=True
    # list of stat on / stat off
    pstats = [True] # only make the plot that includes stat only
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW", ...]')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    parser.add_argument('-x', '--xlim_force',
                        help='Override any algorithms internally deciding xlims for the plots. ["" (default, use algorithms), "0.5", "0.1", ...]')
    parser.add_argument('-l', '--LimitsLegend',
                        help='Add 95% CL limits to the legend? ["y" (default), "n"]')
    parser.add_argument('-fs', '--FileSuffixPlot',
                        help='Optional suffix for plot file (if you want multiple versions).')
    args = parser.parse_args()

    if args.WC is None:
        args.WC = ['cW']
    else:
        WCs = [args.WC]
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    if args.xlim_force is None:
        xlim_force = None
    else:
        xlim_force = float(args.xlim_force)
    if args.LimitsLegend is None:
        limits_legend = True
    else:
        limits_legend = args.LimitsLegend == 'y'
    if args.FileSuffixPlot is None:
        psuff=''
    else:
        psuff = args.FileSuffixPlot
    # loop
    for WC in WCs:
    # for WC in ['cW']: # testing
        print(f'WC: '+WC)
        if WC == 'sm':
            pstats_ = [False]
        else:
            pstats_ = pstats
        if generate_full:
            #####
            print("=========================================================")
            print("Making likelihood plots for full analysis...")
            for pstat in pstats_:
                print(f'Include stat-only? {pstat}')
                fig, ax = run_lim_plot_analysis(WC, datacard_dict, CL_list, ScanType, plot_stat_only=pstat, legend=legend, tight_layout=tight_layout,
                                                vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                                                psuff=psuff, Asimov=Asimov, Unblind=Unblind)
            print("=========================================================\n")
            #'''
    # plt.show()

