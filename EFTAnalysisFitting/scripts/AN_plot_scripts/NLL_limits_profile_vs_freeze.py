# this script mirrors NLL_limits_plot.py, but also plots the stat-only / nosyst likelihood as well.
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import argparse
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator

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

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True

# FIXME! Is "ScanType" needed in this function?
def make_limit_plot(WC, root_file_dict, title, CL_list=[CL_1sigma, 0.95], savefile=None, legend=True, tight_layout=False, xlim_force=None, limits_legend=False):
    # colors
    if 'Asimov' in root_file_dict['prof']:
        c_prof = 'lime'
        c_freeze = 'blue'
    else:
        c_prof = 'purple'
        c_freeze = 'magenta'
    # plot
    #fig = plt.figure(figsize=(16, 8))
    #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    fig, ax = plt.subplots()
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    WC_l = WC_pretty_print_dict[WC]
    # get limits and plot
    # profile
    hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['prof'], WC=WC, extrapolate=True)
    Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
    label = 'Profile Other WCs'
    if limits_legend:
        label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])])# + '\n'
        CL_ = f'{CL_list[0]*100:0.0f}'
        label += f' ({CL_}\% CL)'
    ax.plot(Cs, 2.*NLL, c=c_prof, linestyle='-', linewidth=4, zorder=6, label=label)
    # freeze
    hold_f = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['freeze'], WC=WC, extrapolate=True)
    Cs_f, NLL_f, CL_list_f, NLL_cuts_f, _, _, LLs_f, ULs_f, C_best_f, NLL_best_f = hold_f
    label_f = 'Freeze Other WCs'
    if limits_legend:
        label_f += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_f[0], ULs_f[0])])# + '\n'
        CL_ = f'{CL_list_f[0]*100:0.0f}'
        label_f += f' ({CL_}\% CL)'
    ax.plot(Cs_f, 2.*NLL_f, c=c_freeze, linestyle='-', linewidth=5, zorder=5, label=label_f)
    # loop through CLs to determine limits
    xmin = np.min(Cs)
    xmax = np.max(Cs)
    # if plot_stat_only:
    largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs), np.concatenate(LLs_f), np.concatenate(ULs_f)]))))
    # else:
    #     largest_lim = 1.25*np.max(np.abs(np.array(np.concatenate([np.concatenate(LLs), np.concatenate(ULs)]))))
    xlim = np.max(np.abs([xmin, xmax]))
    xlim2 = np.min(np.abs([xmin, xmax]))
    #if plot_stat_only:
    for CL, NLL_cut, LL, UL, LL_s, UL_s, ls in zip(CL_list, NLL_cuts, LLs, ULs, LLs_f, ULs_f, ['--', '-.', ':',]):
        # build label
        #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
        # multi interval
        label = WC_l+f'@{CL*100:0.1f}\%:\n'
        label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n\n'
        label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL_s, UL_s)]) + '\n(stat. only)\n'
        # add to the plot
        #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
        #        linewidth=3,) #label=label)
        ax.plot([-largest_lim, largest_lim], [2.*NLL_cut, 2.*NLL_cut], 'r', linestyle=ls,
               linewidth=3) #label=label)
    # else:
    #     for CL, NLL_cut, LL, UL, ls in zip(CL_list, NLL_cuts, LLs, ULs, ['--', '-.', ':',]):
    #         # build label
    #         #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]'
    #         # multi interval
    #         label = WC_l+f'@{CL*100:0.1f}\%:\n'
    #         label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n'
    #         # add to the plot
    #         #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
    #         #        linewidth=3,) #label=label)
    #         ax.plot([-largest_lim, largest_lim], [NLL_cut, NLL_cut], 'r', linestyle=ls,
    #                linewidth=3,) #label=label)
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
    ax.set_ylim([-0.01, 2.5*np.max(2*NLL_cuts)])
    # force xlim
    if not xlim_force is None:
        ax.set_xlim([-xlim_force, xlim_force])
    if legend:
        #ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        ax.legend(loc='upper left', framealpha=0.8).set_zorder(9)
    #if tight_layout:
    #    fig.tight_layout()
    # DEBUG!!
    #ax.set_xlim([-1, 1])
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax

def run_lim_plot_analysis(WC, datacard_dict, CL_list, version=None, legend=True, tight_layout=False, vsuff='', xlim_force=None, limits_legend=False, fastScan=False,
                          Asimov=True, Unblind=False):
    # if ScanType == '_1D':
    #     scan_dir = 'freeze'
    #     scan_title = '(Freeze Other WCs)'
    # else:
    #     scan_dir = 'profile'
    #     scan_title = '(Profile Other WCs)'
    scan_dir = 'compare'
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    WC_l = WC_pretty_print_dict[WC]
    if version is None:
        version = 'vCONFIG_VERSIONS'
    version += vsuff
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_full = os.path.join(dcdir, 'output', 'full_analysis')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'full_analysis', scan_dir)
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    # construct root file name
    file_prof = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType='_All',version=version, syst='syst'+FS_suff, method='MultiDimFit')
    file_freeze = template_outfilename.substitute(asimov=asi_output, channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version=version, syst='syst'+FS_suff, method='MultiDimFit')
    root_file_prof = os.path.join(output_dir_full, file_prof)
    root_file_freeze = os.path.join(output_dir_full, file_freeze)
    root_file_dict = {'prof': root_file_prof, 'freeze': root_file_freeze, 'bin_info': None}
    # plot
    #if plot_stat_only:
    #    stat_str = '_w_stat_only'
    #else:
    #    stat_str = ''
    plotfile = os.path.join(plot_dir, f'{asi_prestr}compare_profile_vs_freeze_NLL_vs_{WC}_channel-All_binAll_syst{vsuff}{FS_suff}')
    #title = 'Limits on '+WC_l+f' {scan_title}\nChannel: All; Bin: All'
    title = 'Limits on '+WC_l+f'\nChannel: All; Bin: All'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend)
    return fig, ax


if __name__=='__main__':
    # FIX ME! make these command line args
    #WCs = WC_ALL
    #WCs = ['cW'] # testing
    # confidence level
    CL_list = [0.95, CL_1sigma]
    # which scan type?
    # freeze all but one
    #ScanType = '_1D'
    # profile
    #ScanType = '_All'
    # legend = False
    legend = True
    # tight_layout=False
    tight_layout=True
    # list of stat on / stat off
    pstats = [True] # only make the plot that includes stat only
    # pstats = [True, False] # both
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run make workspaces for?'+
                        '"f" (default). Any combination in any order of the following'+
                        'characters will work: '+
                        '"f" (full analysis).')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["NDIM" (default), "all", "cW", ...]')
    # parser.add_argument('-s', '--ScanType',
    #                     help=f'What strategy was used to handle the other WCs? "_1D" (freeze, default), "_All" (profile)')
    parser.add_argument('-f', '--fastScan',
                        help='Do you want to run a "fast scan" where the nuisance parameters are fixed to best-fit values (instead of profiling)? "n" (default) / "y"')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    parser.add_argument('-x', '--xlim_force',
                        help='Override any algorithms internally deciding xlims for the plots. ["" (default, use algorithms), "0.5", "0.1", ...]')
    parser.add_argument('-l', '--LimitsLegend',
                        help='Add 95% CL limits to the legend? ["n" (default), "y"]')
    args = parser.parse_args()
    # if (args.theLevels is None) or (args.theLevels == 'all'):
    #     generate_bins = True
    #     generate_subch = True
    #     generate_ch = True
    #     generate_full = True
    if (args.theLevels is None):
        generate_bins = False
        generate_subch = False
        generate_ch = False
        generate_full = True
    else:
        generate_bins = False
        generate_subch = False
        generate_ch = False
        '''
        if 'b' in args.theLevels:
            generate_bins = True
        else:
            generate_bins = False
        if 's' in args.theLevels:
            generate_subch = True
        else:
            generate_subch = False
        if 'c' in args.theLevels:
            generate_ch = True
        else:
            generate_ch = False
        '''
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.WC is None:
        args.WC = 'NDIM'
    if args.WC == 'all':
        ##WCs = WC_ALL + ['sm']
        WCs = WC_ALL
    elif args.WC == 'NDIM':
        WCs = WCs_NDIM
    else:
        WCs = [args.WC]
    # if args.ScanType is None:
    #     ScanType = '_1D'
    # else:
    #     ScanType = args.ScanType
    if args.fastScan is None:
        fastScan = False
    else:
        fastScan = args.fastScan == 'y'
    # channels -- for testing
    if args.Channel is None:
        Channel = 'all'
    else:
        Channel = args.Channel
    # all
    if Channel == 'all':
        chs = datacard_dict.keys()
    else:
        chs = [Channel]
    # limited
    #chs = ['2Lepton_SS']
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
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    if args.xlim_force is None:
        xlim_force = None
    else:
        xlim_force = float(args.xlim_force)
    if args.LimitsLegend is None:
        limits_legend = False
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
                                                vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                                                fastScan=fastScan, Asimov=Asimov, Unblind=Unblind)
            print("=========================================================\n")
    # plt.show()

