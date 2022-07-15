# note: this requires uproot, and is typically ran on the GPU machine, rather than the LPC.
import os
import numpy as np
import uproot
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from plotting import config_plots, ticks_in, ticks_sizes

config_plots()
CL_1sigma = 1. - 2.*norm.cdf(-1, loc=0, scale=1)

def get_NLL(root_file):
    file_ = uproot.open(root_file)
    NLL = file_['limit']['deltaNLL'].array()[1:]
    FT0 = file_['limit']['k_cG'].array()[1:]

    return FT0, NLL

def make_limit_plot(FT0, NLL, bin_info, CL_list=[CL_1sigma, 0.95], savefile=None):
    # plot
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.8])
    # plot NLL
    # ax.plot(FT0, NLL, c='blue', linestyle='-', linewidth=2, clip_on=False, label='Expected')
    ax.plot(FT0, NLL, c='blue', linestyle='-', linewidth=2, label='Expected')
    # loop through CLs to determine limits
    xmin = np.min(FT0)
    xmax = np.max(FT0)
    NLL_cuts = []
    LLs = []
    ULs = []
    for CL in CL_list:
        alpha = 1 - CL
        NLL_cut = norm.isf(alpha/2, loc=0, scale=1)**2 / 2
        NLL_cuts.append(NLL_cut)
        # imin = np.argmin(NLL)
        # ft0_best = ft0s[imin]
        # FIXME! do something more clever than this?
        mask_excluded = NLL > NLL_cut
        LL = np.min(FT0[~mask_excluded])
        UL = np.max(FT0[~mask_excluded])
        LLs.append(LL)
        ULs.append(UL)
        # add to the plot
        ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r--', linewidth=2, label=f"FT0: [{LL:0.3f}, {UL:0.3f}]@{CL*100:0.1f}% CL")
    # ax.set_xlabel(r'$f_{T,0}$', fontweight ='bold', loc='right')
    ax.set_xlabel('FT0', fontweight ='bold', loc='right', fontsize=20.)
    ax.set_ylabel('NLL', fontweight='bold', loc='top', fontsize=20.)
    ax.set_title(f'Channel: {bin_info["channel"]}, {bin_info["subchannel"]}; Bin: {bin_info["bin_"]}')
    # ticks
    ax = ticks_in(ax)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax = ticks_sizes(ax, major={'L':15,'W':1.5}, minor={'L':8,'W':1})
    # axis limits
    largest_lim = np.max(np.abs(np.array([LLs, ULs])))
    ax.set_xlim([-2*largest_lim, 2*largest_lim])
    ax.set_ylim([-0.01, 2.5*np.max(NLL_cuts)])
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    # save?
    if not savefile is None:
        fig.savefig(savefile)
    return fig, ax


if __name__=='__main__':
    # file globals
    datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    output_dir = os.path.join(datacard_dir, 'output', 'single_channel_single_bin')
    plot_dir = os.path.join(datacard_dir, 'plots', 'single_channel_single_bin')
    # make paths absolute
    output_dir = os.path.abspath(output_dir)
    # root file
    channel='1lepton'
    subchannel='muon'
    bin_='4'
    bin_info = {'channel':channel, 'subchannel':subchannel, 'bin_':bin_}
    root_file = os.path.join(output_dir, f'higgsCombine_datacard1opWithBkg_FT0_bin{bin_}_{channel}_{subchannel}.MultiDimFit.mH120.root')
    # get NLL
    FT0, NLL = get_NLL(root_file)
    # plot
    savefile = os.path.join(plot_dir, f'{channel}_{subchannel}_bin{bin_}_NLL_vs_FT0.pdf')
    fig, ax = make_limit_plot(FT0, NLL, bin_info=bin_info, CL_list=[0.95, CL_1sigma], savefile=savefile)
    # plt.show()

