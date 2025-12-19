import os
import argparse
from copy import deepcopy
import numpy as np
import uproot
import ROOT
#from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, AutoMinorLocator
import json

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs
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
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title, numerical_formatter, numerical_formatter_with_ndec_return

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True


def make_2D_plot(ddir_out, plot_dir, WC_pair, XYLIM, freeze=True, Asimov=False):
    output_json = {'contours': {}, 'legend': {}}
    type_str = '_tricontour'
    legend_fontsize = 26
    if Asimov:
        asi_str = 'Asimov'
        asi_str_json = 'Asimov'
        asi_str_f = asi_str + '_'
        contour_colors = ['black', 'red']
        #cmap = 'viridis'
    else:
        asi_str = 'Data'
        asi_str_json = 'data'
        # asi_str_f = asi_str + '_'
        asi_str_f = ''
        #contour_colors = ['green', 'magenta']
        contour_colors = ['black', 'blue']
        #cmap = 'hot'
    #print(asi_str)
    WC1, WC2 = WC_pair
    WC_first = WC1
    WC_sec = WC2

    if freeze:
        freeze_str = '_2D'
        freeze_file = 'freeze'
    else:
        freeze_str = '_All2D'
        freeze_file = 'profile'
    print(f'{asi_str}, {freeze_file}')
    ch = 'all'
    version = 'vCONFIG_VERSIONS_NDIM'
    file_scan = ddir_out+f'higgsCombine_{asi_str}.{ch}_combined.{WC_first}_{WC_sec}{freeze_str}.{version}.syst.MultiDimFit.mH120.root'
    s_best = 300
    syst_str = '_syst'
    syst_str_ = 'syst'
    type_str = '_tricontour'
    # load points
    file_ur = uproot.open(file_scan)
    WC1_all = file_ur['limit'][f'k_{WC1}'].array(library='np')
    WC2_all = file_ur['limit'][f'k_{WC2}'].array(library='np')
    NLL_all = file_ur['limit']['deltaNLL'].array(library='np')
    # remove best fit
    WC1_scan = WC1_all[1:]
    WC2_scan = WC2_all[1:]
    NLL_scan = NLL_all[1:]
    # best fit
    WC1_best = WC1_all[0]
    WC2_best = WC2_all[0]
    NLL_best = NLL_all[0]
    # plot
    fsize = (12, 10)
    fig, ax = plt.subplots(figsize=fsize, layout='constrained')
    fig.set_constrained_layout_pads(h_pad=0.0417, w_pad=0.075)
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=False)
    xlim, ylim = XYLIM
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    WC1_p_ = WC_pretty_print_dict[WC1]
    WC2_p_ = WC_pretty_print_dict[WC2]
    WC1_p = WC1_p_ + r'$/\Lambda^2$ [TeV$^{-2}$]'
    WC2_p = WC2_p_ + r'$/\Lambda^2$ [TeV$^{-2}$]'
    ax.set_xlabel(WC1_p)
    ax.set_ylabel(WC2_p)

    l = 'Best fit'
    l += '\n' + rf'{WC1_p_}$/\Lambda^2$ $={WC1_best:0.2f}$ TeV$^{{-2}}$' + '\n' \
    + rf'{WC2_p_}$/\Lambda^2$ $={WC2_best:0.2f}$ TeV$^{{-2}}$'

    ax.scatter([WC1_best], [WC2_best], s=s_best, marker='+', color='red', label=l)
    output_json['contours'][f'{WC1}_best_fit'] = np.float64(WC1_best)
    output_json['contours'][f'{WC2}_best_fit'] = np.float64(WC2_best)
    output_json['legend'][f'{WC1}_best_fit'] = float(f'{WC1_best:0.2f}')
    output_json['legend'][f'{WC2}_best_fit'] = float(f'{WC2_best:0.2f}')

    cr = ax.tricontour(WC1_scan, WC2_scan, 2.*NLL_scan, levels=[2.30, 5.99], colors=contour_colors, zorder=2,
                       linestyles=['--', '-'])

    # calculate overall limits and add to legend
    p0 = cr.get_paths()[0]
    p1 = cr.get_paths()[1]
    # 1 sigma
    v0 = p0.vertices
    x0 = v0[:, 0]
    y0 = v0[:, 1]
    output_json['contours'][f'x_vec_68CL'] = x0.tolist()
    output_json['contours'][f'y_vec_68CL'] = y0.tolist()
    # 2 sigma
    v1 = p1.vertices
    x1 = v1[:, 0]
    y1 = v1[:, 1]
    output_json['contours'][f'x_vec_95CL'] = x1.tolist()
    output_json['contours'][f'y_vec_95CL'] = y1.tolist()

    LL_1 = np.min(x1)
    LL_2 = np.min(y1)
    UL_1 = np.max(x1)
    UL_2 = np.max(y1)
    LL_1_s = numerical_formatter(LL_1)
    LL_2_s = numerical_formatter(LL_2)
    UL_1_s = numerical_formatter(UL_1)
    UL_2_s = numerical_formatter(UL_2)

    output_json['legend'][f'{WC1}_LL_95CL'] = float(LL_1_s)
    output_json['legend'][f'{WC1}_UL_95CL'] = float(UL_1_s)
    output_json['legend'][f'{WC2}_LL_95CL'] = float(LL_2_s)
    output_json['legend'][f'{WC2}_UL_95CL'] = float(UL_2_s)

    handles, labels = cr.legend_elements()
    labels= [r'68$\%$ CL', r'95$\%$ CL']
    hs, ls = ax.get_legend_handles_labels()
    handles = hs + handles
    labels = ls + labels

    limits_label = '\n'+ rf'$[{LL_1_s}, {UL_1_s}]$' + rf' $(${WC1_p_}$/\Lambda^{{2}})$' + '\n'\
    + rf'$[{LL_2_s}, {UL_2_s}]$' + rf' $(${WC2_p_}$/\Lambda^{{2}})$'
    labels[-1] += limits_label

    ax.legend(handles, labels, loc='upper right', fontsize=legend_fontsize,
              ncol=2, columnspacing=1.0, handlelength=1.5,
              labelspacing=1.25,
              bbox_to_anchor=(0.99, 0.925))

    # tick format
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax = ticks_in(ax)
    ax = ticks_sizes(ax, major={'L':10,'W':1.1}, minor={'L':4,'W':0.8})
    # save
    savefile = plot_dir + f'{asi_str_f}2D_limits_{freeze_file}_full_analysis_{ch}_{WC1}_{WC2}{syst_str}{type_str}'
    fig.savefig(savefile+'.pdf')
    fig.savefig(savefile+'.png')
    # json
    with open(savefile+'.json', 'w') as json_file:
        json.dump(output_json, json_file, indent=4)

    return fig, ax


if __name__=='__main__':
    Unblind=True
    WC1s_paper = ['cW', 'cW', 'cHu']
    WC2s_paper = ['cHq3', 'cHl3', 'cHd']
    XYLIMS_dict = {
        'cW_cHq3': [[-0.25, 0.25], [-0.75, 1.5]],
        'cW_cHl3': [[-0.25, 0.25], [-10., 50.0]],
        'cHu_cHd': [[-1.5, 1.5], [-1.5, 4.]],
    }
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w1', '--WC1',
                        help=f'Which Wilson Coefficient on x axis to study for 2D limits? ["cW" (default), "all_paper",...]')
    parser.add_argument('-w2', '--WC2',
                        help=f'Which Wilson Coefficient on y axis to study for 2D limits? ["cHq3" (default), "all_paper", ...]')
    parser.add_argument('-f', '--Freeze',
                        help=f'Freeze other WCs? "y" (default), "n" (profile others)')
    args = parser.parse_args()
    if args.WC1 is None:
        WC1s = ['cW']
    else:
        if args.WC1 == 'all_paper':
            WC1s = WC1s_paper
        else:
            WC1s = [args.WC1]
    if args.WC2 is None:
        WC2s = ['cHq3']
    else:
        if args.WC2 == 'all_paper':
            WC2s = WC2s_paper
        else:
            WC2s = [args.WC2]
    if args.Freeze is None:
        freeze = True
    else:
        freeze = args.Freeze == 'y'

    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    plot_dir = os.path.join(dcdir, 'paper_plots', 'Fig12', '')
    ddir_out = os.path.join(dcdir, 'output', 'full_analysis', '') # where fit files are

    print('Making Fig12 plot(s)...')
    for WC1, WC2 in zip(WC1s, WC2s):
        print(f'{WC1}, {WC2}')
        XYLIM = XYLIMS_dict[f'{WC1}_{WC2}']
        WC_pair = [WC1, WC2]
        fig, ax = make_2D_plot(ddir_out, plot_dir, WC_pair, XYLIM, freeze=freeze, Asimov=False)
    print('Done.')
