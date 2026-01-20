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

# helper functions to get the limits
# get the limits only (syst and stat only)
def get_clipped_lims_full_analysis(ddir_out, clip_ind=0, WC='FT0', CL=0.95, Data=False):
    CL_list = [CL]
    vsuff = f'_clip_mVVV_{clip_ind}'

    if Data:
        asi = 'Data'
    else:
        asi = 'Asimov'

    fname = ddir_out+f'higgsCombine_{asi}.all_combined.{WC}_1D.vCONFIG_VERSIONS{vsuff}.syst.MultiDimFit.mH120.root'
    fname_s = ddir_out+f'higgsCombine_{asi}.all_combined.{WC}_1D.vCONFIG_VERSIONS{vsuff}.nosyst.MultiDimFit.mH120.root'
    try:
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname, WC=WC, extrapolate=True)
        Cs, NLL, CL_list_, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best = _
        LL_ = np.min(LLs_interp[0])
        UL_ = np.max(ULs_interp[0])
    except:
        print(f'Could not load {WC} {asi} {vsuff} syst (job is still running).')
        LL_ = np.nan
        UL_ = np.nan
    try:
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname_s, WC=WC, extrapolate=True)
        Cs_s, NLL_s, CL_list_s, NLL_cuts_s, LLs_s, ULs_s, LLs_interp_s, ULs_interp_s, C_best_s, NLL_best_s = _
        LL_s = np.min(LLs_interp_s[0])
        UL_s = np.max(ULs_interp_s[0])
    except:
        print(f'Could not load {WC} {asi} {vsuff} stat (job is still running).')
        LL_s = np.nan
        UL_s = np.nan
    # collect values
    limit_dict = {'syst': {'LL': LL_, 'UL': UL_}, 'stat': {'LL': LL_s, 'UL': UL_s}}
    return limit_dict

# get the likelihood scans (syst and stat only)
def get_clipped_NLL_full_analysis(ddir_out, clip_ind=0, WC='FT0', CL=0.95, Data=False):
    CL_list = [CL]
    vsuff = f'_clip_mVVV_{clip_ind}'

    if Data:
        asi = 'Data'
    else:
        asi = 'Asimov'

    fname = ddir_out+f'higgsCombine_{asi}.all_combined.{WC}_1D.vCONFIG_VERSIONS{vsuff}.syst.MultiDimFit.mH120.root'
    fname_s = ddir_out+f'higgsCombine_{asi}.all_combined.{WC}_1D.vCONFIG_VERSIONS{vsuff}.nosyst.MultiDimFit.mH120.root'
    try:
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname, WC=WC, extrapolate=True)
        Cs, NLL, CL_list_, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best = _
    except:
        print(f'Could not load {WC} {asi} {vsuff} syst (job is still running).')
        Cs = []
        NLL = []
        NLL_cuts = []
    try:
        _ = get_lims(CL_list, Cs=None, NLL=None, root_file=fname_s, WC=WC, extrapolate=True)
        Cs_s, NLL_s, CL_list_s, NLL_cuts_s, LLs_s, ULs_s, LLs_interp_s, ULs_interp_s, C_best_s, NLL_best_s = _
    except:
        print(f'Could not load {WC} {asi} {vsuff} stat (job is still running).')
        Cs_s = []
        NLL_s = []
    return Cs, NLL, Cs_s, NLL_s, NLL_cuts

# get all limits for various clipping points for plotting
def prepare_clipped_arrays_for_plot(ddir_out, WC, clip_inds, clip_points, CL=0.95, Data=False):
    limit_dict_clip = {}
    LLs = []
    ULs = []
    LLs_s = []
    ULs_s = []
    for clip_ind, clip_point in zip(clip_inds, clip_points):
        limit_dict = get_clipped_lims_full_analysis(ddir_out, clip_ind=clip_ind, WC=WC, CL=CL, Data=Data)
        limit_dict_clip[clip_ind] = limit_dict
        # add to lists
        LLs.append(limit_dict['syst']['LL'])
        ULs.append(limit_dict['syst']['UL'])
        LLs_s.append(limit_dict['stat']['LL'])
        ULs_s.append(limit_dict['stat']['UL'])
    # to arrays
    LLs = np.array(LLs)
    ULs = np.array(ULs)
    LLs_s = np.array(LLs_s)
    ULs_s = np.array(ULs_s)
    # sort by clip value
    #inds = np.arange(len(LLs))
    inds_sort = np.argsort(clip_points)
    clips = clip_points[inds_sort]
    clips_idx = clip_inds[inds_sort]
    LLs = LLs[inds_sort]
    ULs = ULs[inds_sort]
    LLs_s = LLs_s[inds_sort]
    ULs_s = ULs_s[inds_sort]
    return clips, clips_idx, LLs, ULs, LLs_s, ULs_s, limit_dict_clip

def make_clipping_plot(ddir_out, plot_dir, WC, YRANGE, CL, clip_inds, clip_points, unitarity_bounds_one_coeff_dict, unitarity=False):
    output_json = {}
    fig, ax = plt.subplots(figsize=(10,8), layout='constrained')
    fig.set_constrained_layout_pads(h_pad=0.0417, w_pad=0.075)
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=False, inside_frame=False)
    ax.plot([0.6, 5.3], [0., 0.], ':', linewidth=1.5, color='gray') # zero marker
    # unitarity, if available
    if unitarity:
        has_unitarity = WC in unitarity_bounds_one_coeff_dict
        label_unitarity = 'Unitarity bounds'
        if has_unitarity:
            udict = unitarity_bounds_one_coeff_dict[WC]
            coeff = udict['coeff']
            mVVV_power = udict['mVVV_power']
            xs_u = np.linspace(0.1, 6, 601-10)
            ys_u = coeff * 1./xs_u**(mVVV_power)
            # ax.plot(xs_u, ys_u, color='black', linewidth=2, label=label_unitarity)
            # ax.plot(xs_u, -ys_u, color='black', linewidth=2)
            #ax.fill_between(xs_u, -ys_u, ys_u, alpha=0.2, color='gray', label=label_unitarity, edgecolor='black')
            ax.fill_between(xs_u, -ys_u, ys_u, color=(0.1,0.1,0.1, 0.1), label=label_unitarity, edgecolor=(0.,0.,0.,0.4))
            # json
            # output_json[f'x_vec_unitarity'] = xs_u.tolist()
            output_json[f'x_vec_unitarity'] = [round(x, 5) for x in xs_u]
            output_json[f'y_vec_unitarity_LL'] = (-ys_u).tolist()
            output_json[f'y_vec_unitarity_UL'] = ys_u.tolist()

    # loop through asimov and data
    # asimov will include stat only, data just with syst
    for Data, color, legend_lab in zip([False, True], ['blue', 'red'], ['Asimov', 'Data']):
        if legend_lab == 'Data':
            legend_lab_ = legend_lab.lower()
        else:
            legend_lab_ = legend_lab
        if Data:
            asi = 'Data'
        else:
            asi = 'Asimov'
        # get the limits
        _ = prepare_clipped_arrays_for_plot(ddir_out, WC=WC, clip_inds=clip_inds,
                                            clip_points=clip_points, CL=CL, Data=Data)
        clips, clips_idx, LLs, ULs, LLs_s, ULs_s, limit_dict_clip = _
        # remove bad inds -- this script assumes all grid jobs are done
        # bad_inds = bad_index_dict[WC][legend_lab]
        # bi_syst = bad_inds['Syst']
        # bi_stat = bad_inds['Stat']
        # m_syst = ~np.isin(clips_idx, bi_syst)
        # m_stat = ~np.isin(clips_idx, bi_stat)
        # clips_syst = deepcopy(clips)[m_syst]
        clips_syst = deepcopy(clips)
        # LLs = LLs[m_syst]
        # ULs = ULs[m_syst]
        # clips_stat = deepcopy(clips)[m_stat]
        clips_stat = deepcopy(clips)
        # LLs_s = LLs_s[m_stat]
        # ULs_s = ULs_s[m_stat]
        # mask_syst = np.ones(len(inds_sort), np.bool)
        # mask[inds] = 0 # mask bad indices
        # a[mask]
        # handle cases with sign flip
        #ymax = 2. * yrange_dict[WC][1] # FIXME!
        # ymax = 2. * YRANGE[1] # FIXME!
        # m = LLs > ULs
        # LLs[m] = -ymax
        # ULs[m] = ymax
        # m = LLs_s > ULs_s
        # LLs_s[m] = -ymax
        # ULs_s[m] = ymax
        # enforce limit for paper
        if WC in ['cW', 'FT0']:
            LLs[LLs < -100.] = -100.
            LLs_s[LLs_s < -100.] = -100.
            ULs[ULs > 100.] = 100.
            ULs_s[ULs_s > 100.] = 100.


        ## ORIGINAL
        ax.plot(clips_syst*1e-3, LLs, color=color, linewidth=2, label=f'{CL*100:0.0f}'+r'$\%$'+' CL bounds\n'+f'({legend_lab_})')
        #ax.scatter(clips_syst*1e-3, LLs, c=color, s=10)
        ax.plot(clips_syst*1e-3, ULs, color=color, linewidth=2)
        #ax.scatter(clips_syst*1e-3, ULs, c=color, s=10)
        if not Data:
            output_json['x_vec'] = [round(c, 5) for c in clips_syst*1e-3]
        output_json[f'y_vec_LL_syst_{asi}'] = LLs.tolist()
        output_json[f'y_vec_UL_syst_{asi}'] = ULs.tolist()

        if not Data:
            ax.plot(clips_stat*1e-3, LLs_s, '--', color=color, linewidth=2, label=f'{CL*100:0.0f}'+r'$\%$'+' CL bounds\nstatistical only'+f'\n({legend_lab_})')
            #ax.scatter(clips_syst*1e-3, LLs_s, c=color, s=10)
            ax.plot(clips_stat*1e-3, ULs_s, '--', color=color, linewidth=2)
            #ax.scatter(clips_syst*1e-3, LLs_s, c=color, s=10)
            output_json[f'y_vec_LL_stat_{asi}'] = LLs_s.tolist()
            output_json[f'y_vec_UL_stat_{asi}'] = ULs_s.tolist()

        ## WITH POINTS
        # ax.scatter(clips*1e-3, LLs, c=color, s=10, label=f'{CL*100:0.0f}\% CL Limit\n'+f'({legend_lab})')
        # ax.scatter(clips*1e-3, ULs, c=color, s=10)

        # if not Data:
        #     #ax.scatter(clips*1e-3, LLs_s, c=color, s=10, marker='+', label=f'{CL*100:0.0f}\% CL Limit\nStat. Only'+f'\n({legend_lab})')
        #     #ax.scatter(clips*1e-3, ULs_s, c=color, s=10, marker='+')
        #     ax.plot(clips*1e-3, LLs_s, '--', color=color, linewidth=2, label=f'{CL*100:0.0f}\% CL Limit\nStat. Only'+f'\n({legend_lab})')
        #     ax.plot(clips*1e-3, ULs_s, '--', color=color, linewidth=2)
    # plot configs
    ax.set_xlim([0.5, 5.4])
    ax.set_ylim(YRANGE)

    WC_p = WC_pretty_print_dict[WC]

    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    if WC == 'cW':
        ax.yaxis.set_major_locator(MultipleLocator(1.0))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    elif WC == 'FT0':
        ax.yaxis.set_major_locator(MultipleLocator(5.0))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    else:
        #ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax = ticks_in(ax)
    ax = ticks_sizes(ax, major={'L':10,'W':1.1}, minor={'L':4,'W':0.8})
    ax.set_xlabel(r'$m_{\mathrm{VVV}}$ [TeV]', loc='right')
    if WC in dim6_ops:
        yl = rf'{WC_p}/$\Lambda^2$ [TeV$^{{-2}}$]'
    else:
        yl = rf'{WC_p}/$\Lambda^4$ [TeV$^{{-4}}$]'
    ax.set_ylabel(yl, loc='top')
    # legend
    if unitarity:
        handles, labels = ax.get_legend_handles_labels()
        # Define the desired order manually
        dummy = Line2D([], [], color='none')
        #order = []
        # First put Data
        has_data = False
        for label in labels:
            if "data" in label:
                label_d = label
                has_data = True
                break
        if has_unitarity:
            order = [labels.index(label_unitarity)]
        else:
            order = []
        if has_data:
            #order = [labels.index(label_d)]
            order.append(labels.index(label_d))
        for i, l in enumerate(labels):
            if l == label_d or l == label_unitarity:
                continue
            order.append(i)

        if has_unitarity:
            handles_ordered = [handles[o] for o in order]
            labels_ordered = [labels[o] for o in order]
        else:
            handles_ordered = [handles[order[0]], dummy, handles[order[1]], handles[order[2]]]
            labels_ordered = [labels[order[0]], "", labels[order[1]], labels[order[2]]]
        # Apply the reordered legend
        if WC in ['cW', 'FT0']: # paper
            frameon=False
        else: # supplementary
            frameon=True
        ax.legend(handles_ordered,
                  labels_ordered,
                  handlelength=1.0,
                  frameon=frameon, loc='upper right', fontsize=24, ncol=2,
                  bbox_to_anchor=(1.0, 1.0), columnspacing=0.4)
    else:
        handles, labels = ax.get_legend_handles_labels()
        # Define the desired order manually
        dummy = Line2D([], [], color='none')
        #order = []
        # First put Data
        has_data = False
        for label in labels:
            if "data" in label:
                label_d = label
                has_label = True
                break
        order = [labels.index(label_d)]
        for i, l in enumerate(labels):
            if l == label_d:
                continue
            order.append(i)

        handles_ordered = [handles[order[0]], dummy, handles[order[1]], handles[order[2]]]
        labels_ordered = [labels[order[0]], "", labels[order[1]], labels[order[2]]]
        # Apply the reordered legend
        if WC in ['cW', 'FT0']: # paper
            frameon=False
        else: # supplementary
            frameon=True
        ax.legend(handles_ordered,
                  labels_ordered,
                  handlelength=1.0,
                  frameon=frameon, loc='upper right', fontsize=24, ncol=2,
                  bbox_to_anchor=(1.0, 1.0), columnspacing=0.4)
    if WC in dim6_WCs:
        xl = 0.5
        #xm = 7
        xm = 5.4
    else:
        #xl = 1.0
        xl = 0.5
        # xm = 7
        xm = 5.4
    ax.set_xlim([xl, xm])
    # save
    savefile = plot_dir + f'fig_data_{WC}_clipping'
    fig.savefig(savefile+'.pdf')
    fig.savefig(savefile+'.png')
    # json
    with open(savefile+'.json', 'w') as json_file:
        json.dump(output_json, json_file, indent=4)
    # update x range
    savefile = plot_dir + f'fig_data_{WC}_clipping_tightx'
    xrange_orig = ax.get_xlim()
    if WC in dim6_WCs:
        xma = 2.5
    else:
        xma = 3.5
    ax.set_xlim([None, xma])
    fig.savefig(savefile+'.pdf')
    fig.savefig(savefile+'.png')
    # revert for looking at interactively
    ax.set_xlim(xrange_orig)

    return fig, ax


if __name__=='__main__':
    yrange_dict = {
        ### dim6
        'cW': [-5., 5.], 'cHq3': [-6., 6.], 'cHq1': [-9., 9.], 'cHu': [-15., 15.],
        'cHd': [-15., 15.], 'cHW': [-15., 15.], 'cHWB': [-15., 15.], 'cHl3': [-30., 30.],
        'cHB': [-60., 60.], 'cll1': [-60., 60.], 'cHbox': [-260., 260.], 'cHDD': [-220., 220.],
        ### dim8
        'FS0': [-300.,300.], 'FS1': [-300.,300.], 'FS2': [-300.,300.],
        'FM0': [-50.,50.], 'FM1': [-50.,50.], 'FM2': [-200.,200.], 'FM3': [-200.,200.],
        'FM4': [-200.,200.], 'FM5': [-200.,200.], 'FM7': [-300.,300.],
        'FT0': [-15.,15.], 'FT1': [-50.,50.], 'FT2': [-50.,50.], 'FT3': [-50.,50.],
        'FT4': [-75.,75.], 'FT5': [-50.,50.], 'FT6': [-50.,50.], 'FT7': [-75.,75.],
        'FT8': [-200.,200.], 'FT9': [-200.,200.],
    }

    Unblind=True
    CL = 0.95
    WCs_paper = ['cW', 'FT0']
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for clipping limits? ["cW" (default), "FT0", "all_paper", "dim6" , "dim8", "all"...]')
    parser.add_argument('-aux', '--AUX',
                        help=f'Auxilliary plot? "n" (default), "y"')
    parser.add_argument('-uni', '--Unitarity',
                        help='Plot unitarity bounds (as available)? "n" (default), "y"')
    args = parser.parse_args()
    if args.WC is None:
        WCs = ['cW']
    else:
        if args.WC == 'all_paper':
            WC1s = WCs_paper
        elif args.WC == 'dim6':
            WC1s = dim6_WCs
        elif args.WC == 'dim8':
            WC1s = dim8_WCs
        elif args.WC == 'all':
            WC1s = WC_ALL
        else:
            WC1s = [args.WC]
    if args.AUX is None:
        aux = False
    else:
        aux = args.AUX == 'y'
    if args.Unitarity is None:
        unitarity = False
    else:
        unitarity = args.Unitarity == 'y'

    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    if aux:
        plot_dir = os.path.join(dcdir, 'paper_plots', 'clipping', 'clipping_and_unitarity', '')
    else:
        plot_dir = os.path.join(dcdir, 'paper_plots', 'Fig13', '')
    ddir_out = os.path.join(dcdir, 'output', 'full_analysis', '') # where fit files are

    print('Making Fig13 plot(s)...')
    for WC in WC1s:
        print(WC)
        YRANGE = yrange_dict[WC]
        fig, ax = make_clipping_plot(ddir_out, plot_dir, WC, YRANGE, CL,
                                     clip_inds, clip_points,
                                     unitarity_bounds_one_coeff_dict,
                                     unitarity)
    print('Done.')

