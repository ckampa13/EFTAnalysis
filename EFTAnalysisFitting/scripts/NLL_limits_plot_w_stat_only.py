# this script mirrors NLL_limits_plot.py, but also plots the stat-only / nosyst likelihood as well.
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import numpy as np
import uproot
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# local imports
from extract_limits import get_lims, CL_1sigma
from plotting import config_plots, ticks_in, ticks_sizes

config_plots()


def make_limit_plot(root_file_dict, bin_info, CL_list=[CL_1sigma, 0.95], savefile=None):
    # plot
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.8])
    # get limits
    FT0, NLL, CL_list, NLL_cuts, LLs, ULs = get_lims(CL_list, FT0=None, NLL=None, root_file=root_file_dict['total'])
    FT0_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, LLs_stat, ULs_stat = get_lims(CL_list, FT0=None, NLL=None, root_file=root_file_dict['stat_only'])
    # plot NLL
    # total
    ax.plot(FT0, NLL, c='blue', linestyle='-', linewidth=2, label='Expected')
    # stat only
    ax.plot(FT0_stat, NLL_stat, c='blue', linestyle='-.', linewidth=2, label='Expected (stat. only)')
    # loop through CLs to determine limits
    xmin = np.min(FT0)
    xmax = np.max(FT0)
    for CL, NLL_cut, LL, UL, LL_s, UL_s in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat):
        # build label
        # label = f'FT0: [{LL:0.3f}, {UL:0.3f}]@{CL*100:0.1f}% CL\nFT0 (stat. only) [{LL_s:0.3f}, {UL_s:0.3f}]@{CL*100:0.1f}% CL'
        label = f'FT0@{CL*100:0.1f}%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
        # add to the plot
        ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
    # ax.set_xlabel(r'$f_{T,0}$', fontweight ='bold', loc='right')
    ax.set_xlabel('FT0', fontweight ='bold', loc='right', fontsize=20.)
    ax.set_ylabel(r'$\Delta$NLL', fontweight='bold', loc='top', fontsize=20.)
    ax.set_title(f'Channel: {bin_info["channel"]}, {bin_info["subchannel"]}; Bin: {bin_info["bin_"]}')
    # ticks
    ax = ticks_in(ax)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax = ticks_sizes(ax, major={'L':15,'W':1.5}, minor={'L':8,'W':1})
    # axis limits
    largest_lim = 2*np.max(np.abs(np.array([LLs, ULs, LLs_stat, ULs_stat])))
    xlim = np.max(np.abs([xmin, xmax]))
    xlim2 = np.min(np.abs([xmin, xmax]))
    if largest_lim < xlim:
        ax.set_xlim([-largest_lim, largest_lim])
    else:
        # ax.set_xlim([xmin, xmax])
        # ax.set_xlim([-xlim, xlim])
        ax.set_xlim([-xlim2, xlim2])
    ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')
    return fig, ax

def run_lim_plot(bin_info, root_file_dict=None):
    if root_file_dict is None:
        root_file_all = os.path.join(bin_info['output_dir'],
                                     f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                     f'{bin_info["channel"]}_{bin_info["subchannel"]}.MultiDimFit.mH120.root')
        root_file_stat = os.path.join(bin_info['output_dir'],
                                      f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                      f'{bin_info["channel"]}_{bin_info["subchannel"]}_nosyst.MultiDimFit.mH120.root')
        root_file_dict = {'total': root_file_all, 'stat_only': root_file_stat}
    # plot
    savefile = os.path.join(bin_info['plot_dir'], f'{bin_info["channel"]}_{bin_info["subchannel"]}_bin{bin_info["bin_"]}_NLL_vs_FT0_w_stat_only')
    fig, ax = make_limit_plot(root_file_dict, bin_info=bin_info, CL_list=[0.95, CL_1sigma], savefile=savefile)

    # return fig, ax

if __name__=='__main__':
    # file globals
    CHANNEL = '1lepton'
    CHANNEL_DIR = '1Lepton'
    VERSION = 'v1'
    datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    output_dir = os.path.join(datacard_dir, 'output', 'single_channel_single_bin')
    plot_dir = os.path.join(datacard_dir, 'plots', 'single_channel_single_bin', 'include_stat_only')
    # make paths absolute
    datacard_dir = os.path.abspath(datacard_dir)
    output_dir = os.path.abspath(output_dir)
    plot_dir = os.path.abspath(plot_dir)
    # loop through all bins, all channels
    for sc in ["electron", "muon"]:
        for b in [1, 2, 3, 4]:
            # construct bin_info dict
            bin_info = {'output_dir': output_dir, 'plot_dir': plot_dir,
                        'channel': CHANNEL, 'subchannel': sc,
                        'version': VERSION, 'bin_': b,
                        }
            # run analysis / plotting func
            run_lim_plot(bin_info)

    # plt.show()

