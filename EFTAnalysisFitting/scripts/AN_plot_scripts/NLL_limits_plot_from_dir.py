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

config_plots()
plt.rcParams['figure.constrained_layout.use'] = True

# FIXME! Is "ScanType" needed in this function?
def make_limit_plot(WC, root_file_dict, title, CL_list=[CL_1sigma, 0.95], ScanType='_1D', plot_stat_only=True, savefile=None, legend=True, tight_layout=False, xlim_force=None, limits_legend=False, Asimov=True):
    if Asimov:
        c_stat = 'black'
        c_syst = 'blue'
    else:
        c_stat = 'darkgreen'
        c_syst = 'magenta'
    # plot
    #fig = plt.figure(figsize=(16, 8))
    #ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    fig, ax = plt.subplots()
    CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    # get limits and plot
    # total
    hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['total'], WC=WC, extrapolate=True)
    Cs, NLL, CL_list, NLL_cuts, _, _, LLs, ULs, C_best, NLL_best = hold
    label = 'With Systematics'
    if limits_legend:
        label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs[0], ULs[0])])# + '\n'
    ax.plot(Cs, 2.*NLL, c=c_syst, linestyle='-', linewidth=4, zorder=5, label=label)# label='Expected\nAsimov Dataset')
    # stat only
    if plot_stat_only:
        hold = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=root_file_dict['stat_only'], WC=WC, extrapolate=True)
        Cs_stat, NLL_stat, CL_list_stat, NLL_cuts_stat, _, _, LLs_stat, ULs_stat, C_best_stat, NLL_best_stat = hold
        #label='Statistical Uncertainties\nOnly'
        label='Statistical\nUncertainties Only'
        if limits_legend:
            label += '\n'+'\n'.join([f'[{numerical_formatter(LL)}, {numerical_formatter(UL)}]' for LL, UL in zip(LLs_stat[0], ULs_stat[0])])# + '\n'
        ax.plot(Cs_stat, 2.*NLL_stat, c=c_stat, linestyle=':', linewidth=4, zorder=6, label=label)#label='Expected (stat. only)')
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
        for CL, NLL_cut, LL, UL, LL_s, UL_s, ls in zip(CL_list, NLL_cuts, LLs, ULs, LLs_stat, ULs_stat, ['--', '-.', ':',]):
            # build label
            #label = WC_l+f'@{CL*100:0.1f}\%:\n[{LL:0.3f}, {UL:0.3f}]\n[{LL_s:0.3f}, {UL_s:0.3f}] (stat. only)'
            # multi interval
            label = WC_l+f'@{CL*100:0.1f}%:\n'
            label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL, UL)]) + '\n\n'
            label += '\n'.join([f'[{LL_:0.3f}, {UL_:0.3f}]' for LL_, UL_ in zip(LL_s, UL_s)]) + '\n(stat. only)\n'
            # add to the plot
            #ax.plot([xmin, xmax], [NLL_cut, NLL_cut], 'r', linestyle=ls,
            #        linewidth=3,) #label=label)
            ax.plot([-largest_lim, largest_lim], [2.*NLL_cut, 2.*NLL_cut], 'r', linestyle=ls,
                   linewidth=3,) #label=label)
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
            ax.plot([-largest_lim, largest_lim], [2.*NLL_cut, 2.*NLL_cut], 'r', linestyle=ls,
                   linewidth=3,) #label=label)
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
    # force xlim
    if not xlim_force is None:
        ax.set_xlim([-xlim_force, xlim_force])
    if legend:
        #ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        ax.legend(loc='upper left', framealpha=1.0).set_zorder(9)
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
    return fig, ax

def run_lim_plot_bin(WC, channel, subchannel, bin_, datacard_dict, CL_list, ScanType, plot_stat_only, legend, tight_layout, vsuff='', xlim_force=None, limits_legend=False, fastScan=False, psuff='', LinearOnly=False, Asimov=True, Unblind=False, save_vers=False):
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    WC_l = WC_pretty_print_dict[WC]
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_bin = os.path.join(dcdir, 'output', 'single_bin')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'single_bin', scan_dir)
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    # update subchannel name if there is rescaling
    if versions_dict[channel]['lumi'] == '2018':
        sname_sch += '_2018_scaled'
        print(' (2018 scaled)', end='')
    # version number
    #v = versions_dict[channel]['v']
    if vsuff == '_NDIM':
        v = versions_dict[ch]['v_NDIM']
    else:
        v = versions_dict[channel]['v']
    version = f'v{v}'+vsuff
    # plotting info
    bin_info = {'output_dir': output_dir_bin, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': bin_,
                }
    sname_sch_b = sname_sch + f'_bin{bin_}'
    # construct root file name
    # note version number not in single bin single channel output ROOT files. FIXME! Make this consistent.
    file_syst = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType+LinO_str,version=version, syst='syst'+FS_suff, method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel=sname_sch_b, WC=WC, ScanType=ScanType+LinO_str,version=version, syst='nosyst'+FS_suff, method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    pfilename = f'{asi_prestr}NLL_vs_{WC}_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}{ScanType}{vsuff}{FS_suff}{LinO_str}{psuff}'
    if save_vers:
        pfilename += '_' + version
    plotfile = os.path.join(plot_dir, pfilename)
    title = 'Limits on '+WC_l+f' {scan_title}\nChannel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, ScanType=ScanType, plot_stat_only=plot_stat_only, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend, Asimov=Asimov)
    return fig, ax

def run_lim_plot_subchannel(WC, channel, subchannel, datacard_dict, CL_list, ScanType, plot_stat_only, legend, tight_layout, vsuff='', xlim_force=None, limits_legend=False, fastScan=False, psuff='', LinearOnly=False, Asimov=True, Unblind=False, save_vers=False):
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
        LinO_str = ''
    if ScanType == '_1D':
        scan_dir = 'freeze'
        scan_title = '(Freeze Other WCs)'
    else:
        scan_dir = 'profile'
        scan_title = '(Profile Other WCs)'
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    WC_l = WC_pretty_print_dict[WC]
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_sch = os.path.join(dcdir, 'output', 'subchannel')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'subchannel', scan_dir)
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    fname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['file_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    # update subchannel name if there is rescaling
    if versions_dict[channel]['lumi'] == '2018':
        sname_sch += '_2018_scaled'
        print(' (2018 scaled)', end='')
    # version number
    #v = versions_dict[channel]['v']
    if vsuff == '_NDIM':
        v = versions_dict[ch]['v_NDIM']
    else:
        v = versions_dict[channel]['v']
    version = f'v{v}'+vsuff
    bin_info = {'output_dir': output_dir_sch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': fname_sch,
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    file_syst = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType+LinO_str,version=version, syst='syst'+FS_suff, method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType=ScanType+LinO_str,version=version, syst='nosyst'+FS_suff, method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    pfilename = f'{asi_prestr}NLL_vs_{WC}_channel-{channel}_subchannel-{subchannel}_bin{bin_info["bin_"]}{stat_str}{ScanType}{vsuff}{FS_suff}{LinO_str}{psuff}'
    if save_vers:
        pfilename += '_' + version
    plotfile = os.path.join(plot_dir, pfilename)
    title = 'Limits on '+WC_l+f' {scan_title}\nChannel: {bin_info["channel"]}, {subchannel}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, ScanType=ScanType, plot_stat_only=plot_stat_only, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend, Asimov=Asimov)
    return fig, ax

def run_lim_plot_channel(WC, channel, datacard_dict, CL_list, ScantType, plot_stat_only,legend, tight_layout, vsuff='', xlim_force=None, limits_legend=False, fastScan=False, psuff='', LinearOnly=False, Asimov=True, Unblind=False, save_vers=False):
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
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
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_ch = os.path.join(dcdir, 'output', 'channel')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'channel', scan_dir)
    if Asimov:
        asi_prestr = ''
        asi_output = 'Asimov'
    else:
        asi_prestr = 'data_'
        asi_output = 'Data'
    if WC == 'sm':
        asi_output += '_expect_signal_1'
    fname_ch = datacard_dict[channel]['info']['file_name']
    sname_ch = datacard_dict[channel]['info']['short_name']
    # version number
    #v = versions_dict[channel]['v']
    if vsuff == '_NDIM':
        v = versions_dict[ch]['v_NDIM']
    else:
        v = versions_dict[channel]['v']
    version = f'v{v}'+vsuff
    bin_info = {'output_dir': output_dir_ch, 'plot_dir': plot_dir,
                'channel': fname_ch, 'subchannel': 'All',
                'version': version, 'bin_': 'All',
                }
    # construct root file name
    file_syst = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ST,version=version,syst='syst'+FS_suff, method='MultiDimFit')
    file_stat = template_outfilename.substitute(asimov=asi_output, channel=sname_ch, subchannel='_combined', WC=WC, ScanType=ST,version=version,syst='nosyst'+FS_suff, method='MultiDimFit')
    root_file_syst = os.path.join(bin_info['output_dir'], file_syst)
    root_file_stat = os.path.join(bin_info['output_dir'], file_stat)
    root_file_dict = {'total': root_file_syst, 'stat_only': root_file_stat, 'bin_info': bin_info}
    # plot
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    pfilename = f'{asi_prestr}NLL_vs_{WC}_channel-{channel}_bin{bin_info["bin_"]}{stat_str}{ScanType}{vsuff}{FS_suff}{LinO_str}{psuff}'
    if save_vers:
        pfilename += '_' + version
    plotfile = os.path.join(plot_dir, pfilename)
    title = 'Limits on '+WC_l+f' {scan_title}\nChannel: {bin_info["channel"]}, {bin_info["subchannel"]}; Bin: {bin_info["bin_"]}'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, ScanType=ScanType, plot_stat_only=plot_stat_only, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend, Asimov=Asimov)
    return fig, ax

def run_lim_plot_analysis(WC, datacard_dict, CL_list, ScanType, plot_stat_only, version=None, legend=True, tight_layout=False, vsuff='', xlim_force=None, limits_legend=False, fastScan=False, psuff='', LinearOnly=False, channels=[''], Asimov=True, Unblind=False, save_vers=False):
    if LinearOnly:
        LinO_str = '_LinearOnly'
    else:
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
    if fastScan:
        FS_suff = '_fastScan'
    else:
        FS_suff = ''
    if WC == 'sm':
        WC_l = 'SM'
    else:
        WC_l = WC_pretty_print_dict[WC]
    if version is None:
        version = 'vCONFIG_VERSIONS'
    version += vsuff
    if 'tau' in channels:
        dir_ = 'leave_one_out'
        suff_sc = '_LOO_not_tau'
        suff_ch_file = 'Tau'
    else:
        dir_ = 'full_analysis'
        suff_sc = ''
        suff_ch_file = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_full = os.path.join(dcdir, 'output', dir_)
    plot_dir = os.path.join(dcdir, 'AN_plots', dir_, scan_dir)
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
    if plot_stat_only:
        stat_str = '_w_stat_only'
    else:
        stat_str = ''
    pfilename = f'{asi_prestr}NLL_vs_{WC}_channel-All{suff_ch_file}_binAll{stat_str}{ScanType}{vsuff}{FS_suff}{LinO_str}{psuff}'
    if save_vers:
        pfilename += '_' + version
    plotfile = os.path.join(plot_dir, pfilename)
    title = 'Limits on '+WC_l+f' {scan_title}\nChannel: All; Bin: All'
    fig, ax = make_limit_plot(WC, root_file_dict, title, CL_list=CL_list, ScanType=ScanType, plot_stat_only=plot_stat_only, savefile=plotfile,
                              legend=legend, tight_layout=tight_layout, xlim_force=xlim_force, limits_legend=limits_legend, Asimov=Asimov)
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
                        help='Which channel? ["all" (default), "tau", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run make workspaces for?'+
                        '"all" (default). Any combination in any order of the following'+
                        'characters will work: "b" (bin), "s" (subchannel),'+
                        ' "c" (channel), "f" (full analysis). e.g. "bsc" will'+
                        ' run all but the full analysis.')
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["all" (default), "cW", ...]')
    parser.add_argument('-s', '--ScanType',
                        help=f'What strategy was used to handle the other WCs? "_1D" (freeze, default), "_All" (profile)')
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
    parser.add_argument('-fs', '--FileSuffixPlot',
                        help='Optional suffix for plot file (if you want multiple versions).')
    parser.add_argument('-L', '--LinearOnly',
                        help='Drop quadratic and mixed terms in the EFT model? "n" (default), "y"')
    parser.add_argument('-sv', '--SaveVers',
                        help='Save version string in the filename? "n" (default), "y"')
    args = parser.parse_args()
    if (args.theLevels is None) or (args.theLevels == 'all'):
        generate_bins = True
        generate_subch = True
        generate_ch = True
        generate_full = True
    else:
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
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        ##WCs = WC_ALL + ['sm']
        WCs = WC_ALL
    elif args.WC == 'dim6':
        # WCs = []
        # for WC_ in WC_ALL:
        #     if WC_ in dim6_ops:
        #         WCs.append(WC_)
        WCs = dim6_WCs
    elif args.WC == 'dim8':
        # WCs = []
        # for WC_ in WC_ALL:
        #     if not WC_ in dim6_ops:
        #         WCs.append(WC_)
        WCs = dim8_WCs
    elif args.WC == 'tau_profile':
        #WCs = ["cW", "cHq3", "cHq1", "cHu", "cHd", "cHW", "cHWB", "cHl3"]
        #WCs = ["cW", "cHq3", "cHq1"]
        WCs = ["cW", "cHq1", "cHu", "cHd"]
    elif args.WC == 'NDIM':
        WCs = WCs_NDIM
    else:
        WCs = [args.WC]
    if args.ScanType is None:
        ScanType = '_1D'
    else:
        ScanType = args.ScanType
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
    #print(chs)
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
    if args.FileSuffixPlot is None:
        psuff=''
    else:
        psuff = args.FileSuffixPlot
    if args.LinearOnly is None:
        LinearOnly = 'n'
    else:
        LinearOnly = args.LinearOnly
    LinearOnly_bool = LinearOnly == 'y'
    if args.SaveVers is None:
        SaveVers = 'n'
    else:
        SaveVers = args.SaveVers
    SaveVers_bool = SaveVers == 'y'
    # loop
    for WC in WCs:
    # for WC in ['cW']: # testing
        print(f'WC: '+WC)
        if WC == 'sm':
            pstats_ = [False]
        else:
            pstats_ = pstats
        if generate_bins:
            # loop through all bins and plot
            #'''
            print("=========================================================")
            print("Making likelihood plots for each bin...")
            for pstat in pstats_:
                print(f'Include stat-only? {pstat}')
                # for ch in datacard_dict.keys():
                for ch in chs:
                    if WC not in versions_dict[ch]['EFT_ops']:
                        continue
                    print(f'Channel: {ch}')
                    for sch in datacard_dict[ch]['subchannels'].keys():
                        print(f'{sch}: ', end='')
                        for bin_ in datacard_dict[ch]['subchannels'][sch]['bins']:
                            print(f'{bin_} ', end='')
                            fig, ax = run_lim_plot_bin(WC, ch, sch, bin_, datacard_dict, CL_list, ScanType, plot_stat_only=pstat,
                                legend=legend, tight_layout=tight_layout,
                                vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                                fastScan=fastScan, psuff=psuff, LinearOnly=LinearOnly_bool,
                                Asimov=Asimov, Unblind=Unblind, save_vers=SaveVers_bool)
                        print()
            print("=========================================================\n")
        if generate_subch:
            # loop through all subchannels and plot
            print("=========================================================")
            print("Making likelihood plots for each subchannel...")
            for pstat in pstats_:
                print(f'Include stat-only? {pstat}')
                #for ch in datacard_dict.keys():
                for ch in chs:
                    if WC not in versions_dict[ch]['EFT_ops']:
                        continue
                    print(f'Channel: {ch}')
                    for sch in datacard_dict[ch]['subchannels'].keys():
                        print(sch)
                        fig, ax = run_lim_plot_subchannel(WC, ch, sch, datacard_dict, CL_list, ScanType, plot_stat_only=pstat,
                            legend=legend, tight_layout=tight_layout,
                            vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                            fastScan=fastScan, psuff=psuff, LinearOnly=LinearOnly_bool,
                            Asimov=Asimov, Unblind=Unblind, save_vers=SaveVers_bool)
            print("=========================================================\n")
        #'''
        if generate_ch:
            # loop through all channels and plot
            print("=========================================================")
            print("Making likelihood plots for each channel...")
            for pstat in pstats_:
                print(f'Include stat-only? {pstat}')
                #for ch in datacard_dict.keys():
                for ch in chs:
                    if WC != 'sm':
                        if WC not in versions_dict[ch]['EFT_ops']:
                            continue
                    print(ch)
                    fig, ax = run_lim_plot_channel(WC, ch, datacard_dict, CL_list, ScanType, plot_stat_only=pstat,
                        legend=legend, tight_layout=tight_layout,
                        vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                        fastScan=fastScan, psuff=psuff, LinearOnly=LinearOnly_bool,
                        Asimov=Asimov, Unblind=Unblind, save_vers=SaveVers_bool)
            print("=========================================================\n")
        #'''
        if generate_full:
            #####
            print("=========================================================")
            print("Making likelihood plots for full analysis...")
            for pstat in pstats_:
                print(f'Include stat-only? {pstat}')
                fig, ax = run_lim_plot_analysis(WC, datacard_dict, CL_list, ScanType, plot_stat_only=pstat, legend=legend, tight_layout=tight_layout,
                                                vsuff=vsuff, xlim_force=xlim_force, limits_legend=limits_legend,
                                                fastScan=fastScan, psuff=psuff, LinearOnly=LinearOnly_bool, channels=chs,
                                                Asimov=Asimov, Unblind=Unblind, save_vers=SaveVers_bool)
            print("=========================================================\n")
            #'''
    # plt.show()

