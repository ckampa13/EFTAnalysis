# this script mirrors NLL_limits_plot.py, but also plots the stat-only / nosyst likelihood as well.
# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# local imports
from DATACARD_DICT import datacard_dict
from extract_limits import get_lims, CL_1sigma
from plotting import config_plots, ticks_in, ticks_sizes

config_plots()

datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
# make paths absolute
datacard_dir = os.path.abspath(datacard_dir)

def make_limit_plot(root_file_dict, title, CL_list=[CL_1sigma, 0.95], plot_stat_only=True, savefile=None):
    # plot
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.8])
    # get limits and plot
    # total
    FT0, NLL, CL_list, NLL_cuts, LLs, ULs = get_lims(CL_list, FT0=None, NLL=None, root_file=root_file_dict['total'])
    ax.plot(FT0, NLL, c='blue', linestyle='-', linewidth=2, label='Expected')
    # stat only
    if plot_stat_only:
        FT0_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, LLs_stat, ULs_stat = get_lims(CL_list, FT0=None, NLL=None, root_file=root_file_dict['stat_only'])
        ax.plot(FT0_stat, NLL_stat, c='blue', linestyle='-.', linewidth=2, label='Expected (stat. only)')
    # loop through CLs to determine limits
    xmin = np.min(FT0)
    xmax = np.max(FT0)
    if plot_stat_only:
        for CL, NLL_cut, LL, UL, LL_s, UL_s in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat):
            # build label
            label = f'FT0@{CL*100:0.1f}%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
            # add to the plot
            ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
    else:
        for CL, NLL_cut, LL, UL, in zip(CL_list, NLL_cuts, LLs, ULs):
            # build label
            label = f'FT0@{CL*100:0.1f}%:\n[{LL:0.3f}, {UL:0.3f}]'
            # add to the plot
            ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=label)
    ax.set_xlabel('FT0', fontweight ='bold', loc='right', fontsize=20.)
    ax.set_ylabel(r'$\Delta$NLL', fontweight='bold', loc='top', fontsize=20.)
    ax.set_title(title)
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

def run_lim_plot_bin(channel, subchannel, bin_, datacard_dict, version, CL_list, plot_stat_only):
    output_dir_ch = os.path.join(datacard_dir, 'output', 'single_channel_single_bin', channel)
    plot_dir = os.path.join(datacard_dir, 'plots', 'single_channel_single_bin', channel)
    fname_ch = datacard_dict[channel]['info']['file_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': bin_,
                }
    # construct root file name
    # note version number not in single bin single channel output ROOT files. FIXME! Make this consistent.
    root_file_all = os.path.join(bin_info['output_dir'],
                                 f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                 f'{bin_info["channel"]}{bin_info["subchannel"]}.MultiDimFit.mH120.root')
    root_file_stat = os.path.join(bin_info['output_dir'],
                                  f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                  f'{bin_info["channel"]}{bin_info["subchannel"]}_nosyst.MultiDimFit.mH120.root')
    root_file_dict = {'total': root_file_all, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_FT0_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}')
    title = f'Channel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_subchannel(channel, subchannel, datacard_dict, version, CL_list, plot_stat_only):
    output_dir_sch = os.path.join(datacard_dir, 'output', 'combined_datacards', 'subchannel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'combined_datacards', 'subchannel')
    fname_ch = datacard_dict[channel]['info']['file_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    bin_info = {'output_dir': output_dir_sch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    root_file_all = os.path.join(bin_info['output_dir'],
                                 f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                 f'{bin_info["channel"]}{bin_info["subchannel"]}_{bin_info["version"]}.MultiDimFit.mH120.root')
    root_file_stat = os.path.join(bin_info['output_dir'],
                                  f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                  f'{bin_info["channel"]}{bin_info["subchannel"]}_{bin_info["version"]}_nosyst.MultiDimFit.mH120.root')
    root_file_dict = {'total': root_file_all, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_FT0_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}')
    title = f'Channel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_channel(channel, datacard_dict, version, CL_list, plot_stat_only):
    output_dir_ch = os.path.join(datacard_dir, 'output', 'combined_datacards', 'channel')
    plot_dir = os.path.join(datacard_dir, 'plots', 'combined_datacards', 'channel')
    fname_ch = datacard_dict[channel]['info']['file_name']
    bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    root_file_all = os.path.join(bin_info['output_dir'],
                                 f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                 f'{bin_info["channel"]}{bin_info["subchannel"]}_{bin_info["version"]}.MultiDimFit.mH120.root')
    root_file_stat = os.path.join(bin_info['output_dir'],
                                  f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_info["bin_"]}_'+
                                  f'{bin_info["channel"]}{bin_info["subchannel"]}_{bin_info["version"]}_nosyst.MultiDimFit.mH120.root')
    root_file_dict = {'total': root_file_all, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_FT0_channel-{channel}_bin{bin_info["bin_"]}{stat_str}')
    title = f'Channel: {bin_info["channel"]}, {bin_info["subchannel"]}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax

def run_lim_plot_analysis(datacard_dict, version, CL_list, plot_stat_only):
    output_dir_full = os.path.join(datacard_dir, 'output', 'combined_datacards', 'full_analysis')
    plot_dir = os.path.join(datacard_dir, 'plots', 'combined_datacards', 'full_analysis')
    # construct root file name
    root_file_all = os.path.join(output_dir_full,
                                 'higgsCombine_datacard1opWithBkg_FT0_binAll_channelsAll_v1.MultiDimFit.mH120.root')
    root_file_stat = os.path.join(output_dir_full,
                                  'higgsCombine_datacard1opWithBkg_FT0_binAll_channelsAll_v1_nosyst.MultiDimFit.mH120.root')
    root_file_dict = {'total': root_file_all, 'stat_only': root_file_stat, 'bin_info': None}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    plotfile = os.path.join(plot_dir, f'NLL_vs_FT0_channel-All_binAll{stat_str}')
    title = f'Channel: All; Bin: All'
    fig, ax = make_limit_plot(root_file_dict, title, CL_list=CL_list, plot_stat_only=plot_stat_only, savefile=plotfile)
    return fig, ax


if __name__=='__main__':
    # confidence level
    CL_list = [0.95, CL_1sigma]
    VERSION = 'v1'
    # loop through all bins and plot
    print("=========================================================")
    print("Making likelihood plots for each bin...")
    for pstat in [True, False]:
        print(f'Include stat-only? {pstat}')
        for ch in datacard_dict.keys():
            print(f'Channel: {ch}')
            for sch in datacard_dict[ch]['subchannels'].keys():
                print(f'{sch}: ', end='')
                for bin_ in datacard_dict[ch]['subchannels'][sch]['bins']:
                    print(f'{bin_} ', end='')
                    fig, ax = run_lim_plot_bin(ch, sch, bin_, datacard_dict, VERSION, CL_list, plot_stat_only=pstat)
                print()
    print("=========================================================\n")
    # loop through all subchannels and plot
    print("=========================================================")
    print("Making likelihood plots for each subchannel...")
    for pstat in [True, False]:
        print(f'Include stat-only? {pstat}')
        for ch in datacard_dict.keys():
            print(f'Channel: {ch}')
            for sch in datacard_dict[ch]['subchannels'].keys():
                print(sch)
                fig, ax = run_lim_plot_subchannel(ch, sch, datacard_dict, VERSION, CL_list, plot_stat_only=pstat)
    print("=========================================================\n")
    # loop through all channels and plot
    print("=========================================================")
    print("Making likelihood plots for each channel...")
    for pstat in [True, False]:
        print(f'Include stat-only? {pstat}')
        for ch in datacard_dict.keys():
            print(ch)
            fig, ax = run_lim_plot_channel(ch, datacard_dict, VERSION, CL_list, plot_stat_only=pstat)
    print("=========================================================\n")
    #####
    print("=========================================================")
    print("Making likelihood plots for full analysis...")
    for pstat in [True, False]:
        print(f'Include stat-only? {pstat}')
        fig, ax = run_lim_plot_analysis(datacard_dict, VERSION, CL_list, plot_stat_only=pstat)
    print("=========================================================\n")

    # plt.show()

