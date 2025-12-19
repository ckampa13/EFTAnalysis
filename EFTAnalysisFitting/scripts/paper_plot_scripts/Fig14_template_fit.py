import os
#import argparse
from copy import deepcopy
import numpy as np
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

def get_fit_values(ddir_out, file_suff, replace_absurd=False):
    infile = ddir_out + f'multidimfit_TEMPLATES_{file_suff}.root'
    root_in = ROOT.TFile(infile, 'read')

    fit_s = root_in.Get('fit_mdf')
    s_vals = []
    se_vals = []
    se_vals_U = []
    se_vals_D = []
    for i in range(len(bin_centers_rebin)):
    # for i in range(nbins):
        param = fit_s.floatParsFinal().find(f'r_mu_mVVV_b{i+1}')
        s_vals.append(param.getVal())
        se_vals.append(param.getError())
        se_vals_U.append(param.getAsymErrorHi())
        se_vals_D.append(param.getAsymErrorLo())

    root_in.Close()

    s_vals = np.array(s_vals)
    se_vals = np.array(se_vals)
    se_vals_U = np.array(se_vals_U)
    se_vals_D = np.array(se_vals_D)

    # replace absurd values in asym errors?
    se_vals_D_ = deepcopy(se_vals_D)
    se_vals_U_ = deepcopy(se_vals_U)
    if replace_absurd:
        m = ((np.abs(se_vals_D_) < 0.0001) | (np.abs(se_vals_D_) > 0.7))
        se_vals_D_[m] = -se_vals[m]
        m = ((np.abs(se_vals_U_) < 0.0001) | (np.abs(se_vals_U_) > 0.7))
        se_vals_U_[m] = se_vals[m]
    se_vals_U_cleaned = se_vals_U_
    se_vals_D_cleaned = se_vals_D_
    return s_vals, se_vals, se_vals_U, se_vals_D, se_vals_U_cleaned, se_vals_D_cleaned


def make_template_fit_plot(ddir_out, plot_dir, bin_edges_rebin, bin_centers_rebin, band_data=False, band_MC=True):
    output_json = {'bin_edges_TeV': (bin_edges_rebin/1000.).tolist(), 'bin_centers_TeV': (bin_centers_rebin/1000.).tolist()}

    has_unc_label_MC = False
    has_unc_label_data = False

    fig, ax = plt.subplots(figsize=(10, 9.5), layout='constrained')
    CMSify_title(ax, prelim=False, xloc=0.05)
    ax = ticks_in(ax, top_and_right=True)

    xrange = np.max(bin_edges_rebin) - np.min(bin_edges_rebin)

    datas = [True, False, False, False]
    file_suffs = ['DATA_TEST', 'ASIMOV_CW_1p0_TEST', 'ASIMOV_CHQ3_1p0_TEST', 'DATA_ASIMOV_TEST']
    legend_labels = ['Data', 'cW_1p0', 'cHq3_1p0', 'SM']
    cs = ['black', 'red', 'orange', 'blue']
    zorders = [13, 10, 11, 12]
    for data, file_suff, legend_label, c, zorder in zip(datas, file_suffs, legend_labels, cs, zorders):
        print(legend_label)
        output_json[legend_label] = {}
        hold = get_fit_values(ddir_out, file_suff, replace_absurd=False)
        s_vals, se_vals, se_vals_U, se_vals_D, se_vals_U_cleaned, se_vals_D_cleaned = hold
        # step style (no vertical lines)
        ax.hist(bin_centers_rebin/1000., bins=bin_edges_rebin/1000., weights=s_vals, histtype='step', linewidth=1., color=c, zorder=zorder)
        output_json[legend_label]['y_vec'] = s_vals.tolist()
        # labels
        if data:
            label = 'Data'
        elif file_suff == 'DATA_ASIMOV_TEST':
            label = legend_label
        else:
            entries = legend_label.split('_')
            val = float(entries[1].replace('p', '.').replace('m','-'))
            WC = entries[0]
            WC_p = WC_pretty_print_dict_AN[WC]
            # align equals sign for cW and cHq3
            if WC == 'cW':
                pre = r'$\;\;\:$'
            else:
                pre = ''
            label = rf'{WC_p}$/\Lambda^2'+pre+rf'={val:0.1f}$ TeV$^{{-2}}$'
        # how much to shift points for clearer SM and Data
        shift_frac = 0.004
        if data:
            x_shift = - shift_frac * xrange
        else:
            if file_suff == 'DATA_ASIMOV_TEST':
                x_shift = shift_frac * xrange
            else:
                x_shift = 0.
        # plot error band or errorbar
        yerr = [-se_vals_D_cleaned, se_vals_U_cleaned] # errors -- use cleaned values (may be equal to original values)
        output_json[legend_label]['y_vec_uncertainty_up'] = yerr[1].tolist()
        output_json[legend_label]['y_vec_uncertainty_down'] = yerr[0].tolist()
        output_json[legend_label]['x_vec_points'] = (bin_centers_rebin/1000. + x_shift/1000.).tolist()
        if data:
            if band_data:
                ax.plot(bin_centers_rebin/1000. + x_shift/1000., s_vals, 'o', color=c, label=label, zorder=zorder+1)
                if has_unc_label_data:
                    l = None
                else:
                    l = 'Uncertainty (Data)'
                    has_unc_label_data = True
                ax.bar(bin_centers_rebin/1000., yerr[0] + yerr[1], np.diff(bin_edges_rebin/1000.), bottom=s_vals - yerr[0],
                       #color=None, fill=False, edgecolor='gray', hatch='//', linewidth=1,
                       color='black', fill=True, alpha=0.3,
                       label=l, zorder=zorder)
            else:
                ax.errorbar(bin_centers_rebin/1000. + x_shift/1000., s_vals, yerr=yerr, fmt='o', color=c, label=label, zorder=zorder)
        else:
            if band_MC:
                ax.plot(bin_centers_rebin/1000. + x_shift/1000., s_vals, 'o', color=c, label=label, zorder=zorder+1)
                if has_unc_label_MC:
                    l = None
                else:
                    l = 'Uncertainty (MC)'
                    has_unc_label_MC = True
                ax.bar(bin_centers_rebin/1000., yerr[0] + yerr[1], np.diff(bin_edges_rebin/1000.), bottom=s_vals - yerr[0],
                       #color=None, fill=False, edgecolor='gray', hatch='//', linewidth=1,
                       color='gray', fill=True, alpha=0.3,
                       label=l, zorder=zorder)
            else:
                ax.errorbar(bin_centers_rebin/1000. + x_shift/1000., s_vals, yerr=yerr, fmt='o', color=c, label=label, zorder=zorder)
    # plot configs
    ax.set_ylim([-0.14, 1.83])
    ax.set_xticks(bin_centers_rebin/1000.)
    # note the small epsilon added to account for weird python rounding (0.05 rounds to 0.0)
    ax.set_xticklabels([f'{s+0.0001:0.1f}' for s in bin_centers_rebin/1000.])
    ax.xaxis.set_minor_locator(FixedLocator(bin_edges_rebin/1000.))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.grid(False, axis='x')
    ax.grid(False, axis='y')
    ax = ticks_sizes(ax, major={'L':10,'W':1.5}, minor={'L':0,'W':0})
    # update y minor ticks
    ax.tick_params('y', length=5, width=1, which='minor')
    tsize = 28
    ax.tick_params(axis='x', labelsize=tsize)
    ax.tick_params(axis='y', labelsize=tsize)
    # grid lines for bin edges
    ax.xaxis.grid(True, which='minor', linestyle='--', color='gray')
    ax.set_xlabel(r'$m_{\mathrm{VVV}}$ [TeV]', loc='right')
    ax.set_ylabel('Signal strength parameter', loc='top')
    ax.legend(loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.93),
              columnspacing=0.6, handletextpad=0.25, handlelength=1.)
    fig.set_facecolor('white')
    # save
    savefile = plot_dir+'fig_combine_template_fit'
    fig.savefig(savefile+'.pdf')
    fig.savefig(savefile+'.png')
    # json
    with open(savefile+'.json', 'w') as json_file:
        json.dump(output_json, json_file, indent=4)

    # zoomed plot
    ax.set_ylim([-0.1, 0.15])
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    savefile2 = plot_dir+'fig_combine_template_fit_yzoom'
    fig.savefig(savefile2+'.pdf')
    fig.savefig(savefile2+'.png')
    # undo zoom
    ax.set_ylim([-0.14, 1.83])
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))

    return fig, ax


def make_template_fit_txt_dump(ddir_out, plot_dir, bin_edges_rebin, bin_centers_rebin):
    # file we will write to
    savefile = plot_dir + 'template_fit_numerical_vals.txt'
    # add bins to files
    s_bc = '[' + ', '.join([numerical_formatter(b) for b in bin_centers_rebin/1000.]) + ']'
    s_be = '[' + ', '.join([numerical_formatter(b) for b in bin_edges_rebin/1000.]) + ']'
    file_vals_list = [f'Template Fit:\n\nmVVV_bin_centers = {s_bc}\nmVVV_bin_edges = {s_be}\n\n']
    # loop
    datas = [True, False, False, False]
    file_suffs = ['DATA_TEST', 'ASIMOV_CW_1p0_TEST', 'ASIMOV_CHQ3_1p0_TEST', 'DATA_ASIMOV_TEST']
    legend_labels = ['Data', 'cW_1p0', 'cHq3_1p0', 'SM']
    cs = ['black', 'red', 'orange', 'blue']
    zorders = [13, 10, 11, 12]
    for data, file_suff, legend_label, c, zorder in zip(datas, file_suffs, legend_labels, cs, zorders):
        print(legend_label)
        hold = get_fit_values(ddir_out, file_suff, replace_absurd=False)
        s_vals, se_vals, se_vals_U, se_vals_D, se_vals_U_cleaned, se_vals_D_cleaned = hold
        # add to file
        s_v = '['
        s_v_list = []
        for i, tup in enumerate(zip(s_vals, se_vals_U_cleaned, se_vals_D_cleaned)):
            s, eu, ed = tup
            #temp = f'mu{i+1}=' + numerical_formatter(s) + '+' + numerical_formatter(eu) + '-' + numerical_formatter(abs(ed))
            eps = 0.0001 # to avoid 0.5 round down
            if round(eu + eps, 2) < 0.01 or round(abs(ed) + eps, 2) < 0.01:
                # print(f'rounding to 3 decimal places! tup={tup}')
                n = 3
                temp = f'mu{i+1}=' + f'{round(s+eps, n):0.3f}' + '+' + f'{round(eu+eps, n):0.3f}' + '-' + f'{round(abs(ed)+eps, n):0.3f}'
            else:
                n = 2
                temp = f'mu{i+1}=' + f'{round(s+eps, n):0.2f}' + '+' + f'{round(eu+eps, n):0.2f}' + '-' + f'{round(abs(ed)+eps, n):0.2f}'
            s_v_list.append(temp)
        s_v += ', '.join(s_v_list) + ']'
        file_vals_list += [f'{legend_label}:\nBest fit: {s_v}\n\n']
    with open(savefile, 'w') as f:
        f.writelines(file_vals_list)


if __name__=='__main__':
    Unblind=True
    # plot configs
    band_data = False
    # band_data = True
    # band_MC = False
    band_MC = True
    # binning info
    # FIXME! Don't hard code this
    bin_edges_rebin = np.array([0., 2000., 2500., 3000., 3500., 5050.])
    bin_centers_rebin = (bin_edges_rebin[:-1] + bin_edges_rebin[1:])/2.
    # direcotries
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    plot_dir = os.path.join(dcdir, 'paper_plots', 'Fig14', '')
    ddir_out = os.path.join(dcdir, 'output', 'full_analysis', '') # where fit files are
    # plot
    print('Making Fig14 plot...')
    fig, ax = make_template_fit_plot(ddir_out, plot_dir, bin_edges_rebin, bin_centers_rebin,
                                     band_data=band_data, band_MC=band_MC)
    print('Done.\n')
    # txt dump
    print('Dumping to txt file...')
    make_template_fit_txt_dump(ddir_out, plot_dir, bin_edges_rebin, bin_centers_rebin)
    print('Done.\n')
