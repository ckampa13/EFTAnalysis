import os
import argparse
from copy import deepcopy
import numpy as np
import uproot
import ROOT
#from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, AutoMinorLocator
from matplotlib.lines import Line2D
import json

# local imports
from unitarity_dim8 import unitarity_bounds_one_coeff_dict
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
    clip_inds,
    clip_points
)
WC_pretty_print_dict = WC_pretty_print_dict_AN
SR_pretty_print_dict = SR_pretty_print_dict_AN
#from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title, numerical_formatter, numerical_formatter_with_ndec_return

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True

def find_mVVV_at_WC_val(val, coeff, mVVV_power):
    return (coeff/val)**(1/mVVV_power)

def make_unitarity_plot(plot_dir, WC, unitarity_bounds_one_coeff_dict):
    WC_p = WC_pretty_print_dict[WC]
    fig, ax = plt.subplots(figsize=(10,8), layout='constrained')
    fig.set_constrained_layout_pads(h_pad=0.0417, w_pad=0.075)
    # CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True, inside_frame=False)
    # ax.plot([0.6, 5.3], [0., 0.], ':', linewidth=1.5, color='gray') # zero marker
    # unitarity, if available
    #has_unitarity = WC in unitarity_bounds_one_coeff_dict
    label_unitarity = 'Unitarity bounds'
    udict = unitarity_bounds_one_coeff_dict[WC]
    coeff = udict['coeff']
    mVVV_power = udict['mVVV_power']
    x_at_1 = find_mVVV_at_WC_val(val=1, coeff=coeff, mVVV_power=mVVV_power)
    x_at_10 = find_mVVV_at_WC_val(val=10, coeff=coeff, mVVV_power=mVVV_power)
    xs_u = np.linspace(0.5, 2.*x_at_1, 500)
    ys_u = coeff * 1./xs_u**(mVVV_power)
    # ax.plot(xs_u, ys_u, color='black', linewidth=2, label=label_unitarity)
    # ax.plot(xs_u, -ys_u, color='black', linewidth=2)
    #ax.fill_between(xs_u, -ys_u, ys_u, alpha=0.2, color='gray', label=label_unitarity, edgecolor='black')
    ax.fill_between(xs_u, -ys_u, ys_u, color=(0.1,0.1,0.1, 0.1), label=label_unitarity, edgecolor=(0.,0.,0.,0.4))

    ax.scatter(2*[x_at_1], [1., -1.], c='blue', marker='*', s=50, label='\nBound Location:\n'+rf'{WC_p}/$\Lambda^4 = \pm 1$ TeV$^{{-4}}$'+'\n'+r'$m_{\text{VVV}} = $' + f'{x_at_1:0.1f} TeV\n')
    ax.scatter(2*[x_at_10], [10., -10.], c='red', marker='^', s=50, label='\nBound Location:\n'+rf'{WC_p}/$\Lambda^4 = \pm 10$ TeV$^{{-4}}$'+'\n'+r'$m_{\text{VVV}} = $' + f'{x_at_10:0.1f} TeV\n')

    # plot configs
    # ax.set_xlim([0.5, 5.4])
    # ax.set_ylim(YRANGE)

    ax.set_ylim([-20, 20])
    ax.set_xlim([xs_u.min(), xs_u.max()])

    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    if WC == 'FT0':
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    elif WC == 'FS0':
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    elif WC == 'FM0':
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))


    # ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    # if WC == 'cW':
    #     ax.yaxis.set_major_locator(MultipleLocator(1.0))
    #     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    # elif WC == 'FT0':
    #     ax.yaxis.set_major_locator(MultipleLocator(5.0))
    #     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    # else:
    #     #ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    #     ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax = ticks_in(ax)
    ax = ticks_sizes(ax, major={'L':10,'W':1.1}, minor={'L':4,'W':0.8})
    ax.set_xlabel(r'$m_{\mathrm{VVV}}$ [TeV]', loc='right')
    if WC in dim6_ops:
        yl = rf'{WC_p}/$\Lambda^2$ [TeV$^{{-2}}$]'
    else:
        yl = rf'{WC_p}/$\Lambda^4$ [TeV$^{{-4}}$]'
    ax.set_ylabel(yl, loc='top')
    # legend
    # handles, labels = ax.get_legend_handles_labels()
    # Define the desired order manually
    # dummy = Line2D([], [], color='none')
    #order = []
    # First put Data
    # has_data = False
    # for label in labels:
    #     if "data" in label:
    #         label_d = label
    #         has_data = True
    #         break
    # if has_unitarity:
    #     order = [labels.index(label_unitarity)]
    # else:
    #     order = []
    # if has_data:
    #     #order = [labels.index(label_d)]
    #     order.append(labels.index(label_d))
    # for i, l in enumerate(labels):
    #     if l == label_d or l == label_unitarity:
    #         continue
    #     order.append(i)

    # if has_unitarity:
    #     handles_ordered = [handles[o] for o in order]
    #     labels_ordered = [labels[o] for o in order]
    # else:
    #     handles_ordered = [handles[order[0]], dummy, handles[order[1]], handles[order[2]]]
    #     labels_ordered = [labels[order[0]], "", labels[order[1]], labels[order[2]]]
    # # Apply the reordered legend
    # if WC in ['cW', 'FT0']: # paper
    #     frameon=False
    # else: # supplementary
    #     frameon=True
    # ax.legend(handles_ordered,
    #           labels_ordered,
    #           handlelength=1.0,
    #           frameon=frameon, loc='upper right', fontsize=24, ncol=2,
    #           bbox_to_anchor=(1.0, 1.0), columnspacing=0.4)
    dummy = Line2D([], [], color='none')
    handles, labels = ax.get_legend_handles_labels()
    handles_n = [handles[0], dummy, handles[1], handles[2]]
    labels_n = [labels[0], "", labels[1], labels[2]]
    ax.legend(handles_n, labels_n, loc='upper right', fontsize=18,
              ncol=2, columnspacing=0.4, frameon=False)
    # if WC in dim6_WCs:
    #     xl = 0.5
    #     #xm = 7
    #     xm = 5.4
    # else:
    #     #xl = 1.0
    #     xl = 0.5
    #     # xm = 7
    #     xm = 5.4
    # ax.set_xlim([xl, xm])
    # save
    savefile = plot_dir + f'{WC}_unitarity'
    fig.savefig(savefile+'.pdf')
    fig.savefig(savefile+'.png')
    # json
    # with open(savefile+'.json', 'w') as json_file:
    #     json.dump(output_json, json_file, indent=4)
    # # update x range
    # savefile = plot_dir + f'fig_data_{WC}_clipping_tightx'
    # xrange_orig = ax.get_xlim()
    # if WC in dim6_WCs:
    #     xma = 2.5
    # else:
    #     xma = 3.5
    # ax.set_xlim([None, xma])
    # fig.savefig(savefile+'.pdf')
    # fig.savefig(savefile+'.png')
    # # revert for looking at interactively
    # ax.set_xlim(xrange_orig)

    return fig, ax


if __name__=='__main__':
    # yrange_dict = {
    #     ### dim6
    #     'cW': [-5., 5.], 'cHq3': [-6., 6.], 'cHq1': [-9., 9.], 'cHu': [-15., 15.],
    #     'cHd': [-15., 15.], 'cHW': [-15., 15.], 'cHWB': [-15., 15.], 'cHl3': [-30., 30.],
    #     'cHB': [-60., 60.], 'cll1': [-60., 60.], 'cHbox': [-260., 260.], 'cHDD': [-220., 220.],
    #     ### dim8
    #     'FS0': [-300.,300.], 'FS1': [-300.,300.], 'FS2': [-300.,300.],
    #     'FM0': [-50.,50.], 'FM1': [-50.,50.], 'FM2': [-200.,200.], 'FM3': [-200.,200.],
    #     'FM4': [-200.,200.], 'FM5': [-200.,200.], 'FM7': [-300.,300.],
    #     'FT0': [-15.,15.], 'FT1': [-50.,50.], 'FT2': [-50.,50.], 'FT3': [-50.,50.],
    #     'FT4': [-75.,75.], 'FT5': [-50.,50.], 'FT6': [-50.,50.], 'FT7': [-75.,75.],
    #     'FT8': [-200.,200.], 'FT9': [-200.,200.],
    # }

    Unblind=True
    CL = 0.95
    WCs_test = ['FS0', 'FM0', 'FT0']
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to make unitarity plot for? ["test" (default), "FT0", "FT1", ...]')
    args = parser.parse_args()
    if args.WC is None:
        WCs = WCs_test
    else:
        if args.WC == 'test':
            WC1s = WCs_test
        elif args.WC == 'dim8':
            WC1s = dim8_WCs
        else:
            WC1s = [args.WC]

    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    plot_dir = os.path.join(dcdir, 'paper_plots', 'clipping', 'unitarity', '')

    print('Making unitarity plot(s)...')
    for WC in WC1s:
        print(WC)
        # YRANGE = yrange_dict[WC]
        fig, ax = make_unitarity_plot(plot_dir, WC, unitarity_bounds_one_coeff_dict)
    print('Done.')

