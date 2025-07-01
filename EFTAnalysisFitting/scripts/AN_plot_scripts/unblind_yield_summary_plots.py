# this script reads the .pkl tables generated in VVVYieldTable
# FIXME! This code should all be in the same repo.
import os
import argparse
from copy import deepcopy
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
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
# from tools.extract_limits import get_lims, get_lims_w_best, CL_1sigma
#from tools.extract_limits_multi_interval import get_lims, get_lims_w_best, CL_1sigma
from tools.plotting_AN import config_plots, ticks_in, ticks_sizes, CMSify_title
#from process_yields_limits import process_yields_limits

config_plots()

# FIXME! Don't hard code this.
#tabledir = '/home/ckampa/coding/VVVTable/EFT_yields/data/'
tabledir = os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output', 'dataframes'))

def bin_ranked_yield_histo_bkg_combined(tablepkl, WC, datacard_dict, versions_dict, logy=False, channel_rank=False, limit_rank=True, sm_significance=False, savefile=None, NTOYS=200, Unblind=True, use_fit='postfit'):
    # load table
    # add option to creat on the fly?
    #df_yields = process_yields_limits(WC, datacard_dict, versions_dict, NTOYS=NTOYS, Unblind=Unblind)
    df_yields = pd.read_pickle(tablepkl)
    # load table
    # pkl
    #if ".pkl" in tablepkl:
    #    df_yields = pd.read_pickle(tablepkl)
    #elif ".csv" in tablepkl:
    #    df_yields = pd.read_csv(tablepkl)
    #    df_yields.fillna('', inplace=True)
    #else:
    #    raise ValueError("A pickle or csv file was expected (.pkl or .csv respectively). #Please input a valid file name.")
    # add bin label for the plot
    # FIXME! should this go in the original yield table generation?
    df_yields_new = []
    for channel, ch_dict in datacard_dict.items():
        if WC not in versions_dict[channel]['EFT_ops']:
            continue
        sname_ch = ch_dict['info']['short_name']
        sch_dict = ch_dict['subchannels']
        for subchannel in sch_dict.keys():
            print(channel, subchannel)
            sname_sch = sch_dict[subchannel]['info']['short_name']
            m = (df_yields.channel == channel) & (df_yields.subchannel == subchannel)
            df_yields.loc[m, 'bin_label'] = [f'{sname_ch}{sname_sch}_bin{row.bin}' for row in df_yields.loc[m, :].itertuples()]
            # grab a process
            procs = df_yields.loc[m, 'process'].unique()
            df_ = df_yields[m].query(f'process == "{procs[0]}"')
            df_yields_new.append(df_)
    df_yields = pd.concat(df_yields_new, ignore_index=True, axis=0)
    # DEBUG
    #print(f'After processing: df_yields=')
    #print(f'{df_yields}')

    # take an average of some of the two-sided values
    #fit = 'Data'
    #if use_fit == 'postfit':
    #    fit = 'Data'
    #else:
    #    fit = 'Asimov'
    fit = 'Data'
    df_yields.loc[:, f'yield_{WC}_95CL_{fit}'] = (df_yields.loc[:, f'yield_{WC}_95CL_UL_{fit}'] + df_yields.loc[:, f'yield_{WC}_95CL_LL_{fit}']) / 2.
    df_yields.loc[:, f'comb_yield_{WC}_95CL_{fit}'] = (df_yields.loc[:, f'comb_yield_{WC}_95CL_UL_{fit}'] + df_yields.loc[:, f'comb_yield_{WC}_95CL_LL_{fit}']) / 2.
    # DEBUG
    # print(df_yields[f'comb_yield_{WC}_95CL_UL_{fit}'])
    # print(df_yields[f'comb_yield_{WC}_95CL_{fit}'])
    # print(df_yields.loc[:, f'yield_sm_{use_fit}'])
    # print(df_yields.loc[:, f'comb_yield_{WC}_95CL_{fit}'].values - df_yields.loc[:, f'yield_sm_{use_fit}'].values)
    df_yields.loc[:, f'{WC}_95CL_{fit}'] = (df_yields.loc[:, f'{WC}_95CL_UL_{fit}'].abs() + df_yields.loc[:, f'{WC}_95CL_LL_{fit}'].abs()) / 2.
    df_yields.loc[:, f'comb_{WC}_95CL_{fit}'] = (df_yields.loc[:, f'comb_{WC}_95CL_UL_{fit}'].abs() + df_yields.loc[:, f'comb_{WC}_95CL_LL_{fit}'].abs()) / 2.
    # 95% CL values -- full combination
    limit_95CL = df_yields.loc[:, f'all_comb_{WC}_95CL_UL_{fit}'].iloc[0]
    limit_95CL_UL = df_yields.loc[:, f'all_comb_{WC}_95CL_UL_{fit}'].iloc[0]
    limit_95CL_LL = df_yields.loc[:, f'all_comb_{WC}_95CL_LL_{fit}'].iloc[0]
    yield_95CL_min_SM = df_yields.loc[:, f'all_comb_yield_{WC}_95CL_UL_{fit}'] - df_yields.loc[:, f'sm_{WC}']
    df_yields.loc[:, f'all_comb_yield_{fit}'] = yield_95CL_min_SM
    total_bkg_plu_SM = df_yields.loc[:, f'total_bkg_{use_fit}'] + df_yields.loc[:, f'yield_sm_{use_fit}']
    df_yields.loc[:, f'total_bkg_plu_SM_{use_fit}'] = total_bkg_plu_SM
    # full analysis
    # do I need this one?
    ##df_yields.loc[:, 'total_syst'] = (df_yields.loc[:, 'total_syst_Up'] + df_yields.loc[:, 'total_syst_Down']) / 2.
    # calculate median significance (approx.) -- from Cowan, Cranmer, et al. Equation 97.
    # at exclusion
    # with sm in background
    s = df_yields.loc[:, f'comb_yield_{WC}_95CL_{fit}'] - df_yields.loc[:, f'yield_sm_{use_fit}']
    b = df_yields.loc[:, f'total_bkg_{use_fit}'] + df_yields.loc[:, f'yield_sm_{use_fit}']
    # DEBUG
    #print(f's={s}, b={b}')
    df_yields.loc[:, f'med_sig_{WC}_{use_fit}'] = (2 * ((s + b)\
                                              * np.log(1 + s/b)\
                                              - s))**(1/2)
    # at sm
    df_yields.loc[:, f'sm_sig_{use_fit}'] = (2 * ((df_yields.loc[:, f'yield_sm_{use_fit}'] + df_yields.loc[:, f'total_bkg_{use_fit}'])\
                                              * np.log(1 + df_yields.loc[:, f'yield_sm_{use_fit}']/df_yields.loc[:, f'total_bkg_{use_fit}'])\
                                              - df_yields.loc[:, f'yield_sm_{use_fit}']))**(1/2)
    # sort!
    # use limits?
    if limit_rank:
        WC_l = WC_pretty_print_dict[WC]
        ylabel = rf'{WC_l}'+' Limit\n95\% CL'
        ysymm = True
        # channel rank?
        if channel_rank:
            # FIXME! This is to get AN done but is misleading flag now.
            sort_cols = [f'comb_{WC}_95CL_{fit}', 'bin_label']
            asc_list = [False, True]
        else:
            sort_cols = [f'{WC}_95CL_{fit}']
            asc_list = [False]
        ycol_cW = f'all_comb_yield_{fit}'
        lab_cW = f'VVV Yield\n(Total - SM)\n'+rf'{WC_l}'+rf'$={limit_95CL:0.3f}$'#+' (95\% CL UL)\n'+r'$-$SM VVV'
    # use median significance
    # note here channel ranking will still rely on combine output
    else:
        if sm_significance:
            ylabel = f'SM Significance\n({WC}=0)'
            ycol = f'sm_sig_{use_fit}'
            ysymm = False
            # channel rank?
            if channel_rank:
                sort_cols = [f'comb_{WC}_95CL_{fit}', f'sm_sig_{use_fit}']
                asc_list = [False, True]
            else:
                sort_cols = [f'sm_sig_{use_fit}']
                asc_list = [True]
            ycol_cW = f'yield_sm_{use_fit}'
            lab_cW = f'{WC}=0.0 (SM)'
        else:
            ylabel = f'Median Significance\n{WC} Exclusion Point\n95\% CL'
            ycol = f'med_sig_{WC}_{use_fit}'
            ysymm = False
            # channel rank?
            if channel_rank:
                sort_cols = [f'comb_{WC}_95CL_{fit}', f'med_sig_{WC}_{use_fit}']
                asc_list = [False, True]
            else:
                sort_cols = [f'med_sig_{WC}_{use_fit}']
                asc_list = [True]
            ycol_cW = f'all_comb_yield_{fit}'
            lab_cW = f'Yield @ {WC}={limit_95CL:0.3f} (95\% CL UL)\n'+r'$-$SM VVV'
    df_yields.sort_values(by=sort_cols, ascending=asc_list, inplace=True)
    # don't include dummy bins (b = 0, s = 0) -- appear in early versions of tau channels
    df_yields = df_yields.query(f'total_bkg_{use_fit} > 1e-3').copy()
    # reset index
    df_yields.reset_index(drop=True, inplace=True)

    # plot
    #fig = plt.figure(figsize=(18, 16))
    fig = plt.figure(figsize=(18, 16), layout='constrained')
    axs = []
    axs.append(fig.add_axes((0.1, 0.44, 0.6, 0.45)))
    axs.append(fig.add_axes((0.1, 0.20, 0.6, 0.22))) #, sharex=ax1)
    CMSify_title(axs[0], lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True)
    ticks_in(axs[0])
    ticks_in(axs[1])
    # for the combined limit bin
    # try inset axis
    #axin = axs[1].inset_axes([1.1, 0.0, 0.1, 1.0])
    axin = axs[1].inset_axes([1.1, 0.3, 0.1, 1.0])
    axs.append(axin)
    df_yields.loc[:, 'channel_subchannel'] = df_yields.loc[:, 'channel'] + df_yields.loc[:, 'subchannel']
    if channel_rank:
        delta = 0.75
        prev = 0.
        inds = []
        bin_edges = []
        xticklabels = []
        for i in df_yields.channel_subchannel.unique():
            df_s = df_yields.query(f'channel_subchannel == "{i}"')
            nbins = len(df_s)
            inds.append(delta + np.arange(prev+1, prev+nbins+1, 1))
            bin_edges.append(delta+np.arange(prev, prev+nbins+1, 1) + 0.5)
            # only one xticklabel
            ch_ = '_'.join(df_s['bin_label'].values[0].split('_')[:-1])
            ch_label = SR_pretty_print_dict[ch_]
            ticklabels = deepcopy(df_s['bin_label'].values)
            Nt = len(ticklabels)
            ticklabels[:Nt//2-1] = ''
            ticklabels[Nt//2-1] = ch_label
            ticklabels[Nt//2:] = ''
            xticklabels.append(np.concatenate([[""], ticklabels]))
            prev = inds[-1][-1]
        inds = np.concatenate(inds)
        bin_edges = np.concatenate(bin_edges)
        xticklabels = np.concatenate(xticklabels)
        inds_bot = np.concatenate([inds, [inds[-1]+2]])
        bin_edges_bot = np.concatenate([bin_edges, [bin_edges[-1]+1, bin_edges[-1]+2]])
        xticklabels_bot = np.concatenate([xticklabels, ['', 'Combined Limit']])
    else:
        inds = list(df_yields.index)
        bin_edges = np.arange(inds[0] - 0.5, inds[-1] + 1.5, 1.0)
        xticklabels = np.concatenate([[''], df_yields['bin_label'].values])
        inds_bot = np.concatenate([inds, [inds[-1]+1]])
        bin_edges_bot = np.concatenate([bin_edges, [bin_edges[-1]+1]])
        xticklabels_bot = np.concatenate([xticklabels, ['Combined Limit']])
    # plot background
    # background with sm
    axs[0].hist(inds, bins=bin_edges, weights=df_yields[f'total_bkg_plu_SM_{use_fit}'], histtype='bar', color='khaki', alpha=0.7, label=f'Total Background\n({use_fit.capitalize()})', zorder=10)
    #axs[0].errorbar(inds, df_yields[f'total_bkg_plu_SM_{fit}'], yerr=df_yields[[f'total_bkg_err_{use_fit}', f'total_bkg_err_{use_fit}']].values.T,
    #                marker='', ls='none', color='black', elinewidth=3,
    #                label='Systematics', zorder=12)
    # plot MC stat error as hatched bar
    # error as hatched bar
    axs[0].bar(inds, 2*df_yields[f'total_bkg_err_{use_fit}'].values, 1.0, bottom=df_yields[f'total_bkg_plu_SM_{use_fit}']-df_yields[f'total_bkg_err_{use_fit}'].values,
               color=None, fill=False, edgecolor='cornflowerblue', hatch='//', linewidth=1, label='Uncertainty (SM)', zorder=11)
    # WC @ 95% exclusion
    axs[0].hist(inds, bins=bin_edges, weights=df_yields[ycol_cW].values, histtype='step', color='red', linewidth=2, label=lab_cW, zorder=13)
    # data
    m = (df_yields['data'] > 0)
    axs[0].errorbar(inds[m], df_yields.loc[m, 'data'].values, yerr=(df_yields.loc[m,'data_err_D'], df_yields.loc[m,'data_err_U']), c='black',
                    fmt='o', ls='none', ms=6, zorder=100, capsize=4,
                    label='Data')
    # exclusion
    #fit_ = 'Asimov'
    #for fit_, yl, c, ec, zorder_ in zip(['Asimov', 'Data'], ['Expected', 'Observed'], [None, 'salmon'], ['black', 'salmon'], [11, 10]):
    # exp_c = 'black'
    exp_c = 'gray'
    for fit_, yl, c, fill, hatch, m, mc, zorder_ in zip(['Asimov', 'Data'], ['Expected', 'Observed'], [exp_c, 'salmon'], [False, True], ['//', None], ['*', '^'], ['black', 'yellow'], [11, 10]):
        # if ec == 'black':
        #     ec_c = 'blue'
        #     c_c = None
        # else:
        #     ec_c = 'red'
        #     c_c = ec_c
        if c == exp_c:
            c_c = 'blue'
            fill_c = False
        else:
            c_c = 'red'
            fill_c = fill
        if limit_rank:
            yheight = (df_yields[f'{WC}_95CL_UL_{fit_}'] - df_yields[f'{WC}_95CL_LL_{fit_}']).values
            ybot = df_yields[f'{WC}_95CL_LL_{fit_}'].values
        else:
            yheight = df_yields.loc[:, ycol].values
            ybot = np.zeros_like(df_yields.loc[:,ycol])
        axs[1].bar(inds_bot[:-1], yheight, 1.0, bottom=ybot, color=c, edgecolor=c, fill=fill, hatch=hatch, zorder=zorder_, label=yl+' (bin)')
        # combined
        limit_95CL_LL_ = df_yields.loc[:, f'all_comb_{WC}_95CL_LL_{fit_}'].iloc[0]
        limit_95CL_UL_ = df_yields.loc[:, f'all_comb_{WC}_95CL_UL_{fit_}'].iloc[0]
        height = limit_95CL_UL_ - limit_95CL_LL_
        max_l = max([abs(limit_95CL_UL_), abs(limit_95CL_LL_)])
        axs[1].bar([inds_bot[-1]], height, 1.0, bottom=limit_95CL_LL_, color=c_c, edgecolor=c_c, fill=fill_c, hatch=hatch, zorder=zorder_, label=yl+' (combined)')
        # add combined limit in it's own axis
        axs[2].bar(inds_bot[-1], height, 1.0, bottom=limit_95CL_LL_, color=c_c, edgecolor=c_c, fill=fill_c, hatch=hatch, zorder=zorder_)
        # best fit
        if fit_ == 'Asimov':
            z_ = zorder_ + 2
        else:
            z_ = zorder_ + 4
        best_fit = df_yields[f'{WC}_best_fit_{fit_}'].iloc[0]
        axs[1].scatter([inds_bot[-1]], [best_fit], marker=m, c=mc, s=50, edgecolor='black', zorder=z_, label=yl+' (best fit)')
        axs[2].scatter([inds_bot[-1]], [best_fit], marker=m, c=mc, s=100, edgecolor='black', zorder=z_)
    axs[2].set_ylim([-2*max_l, 2*max_l])
    axs[2].set_xlim([inds_bot[-1]-2, inds_bot[-1]+2])
    # ticks
    # right side for combined limit
    axs[2].yaxis.tick_right()
    # limits
    # symm y
    ym = df_yields[[f'{WC}_95CL_LL_{fit}', f'{WC}_95CL_UL_{fit}']].abs().max().max()
    yr = df_yields[f'{WC}_95CL_UL_{fit}'].max()-df_yields[f'{WC}_95CL_LL_{fit}'].min()
    if ysymm:
        axs[1].set_ylim([-ym-0.1*yr, ym+0.1*yr])
    # FIXME! Check carefully if this is what I want
    axs[1].set_ylim([-20 * max_l, 20 * max_l])
    # WC specific? -- debug
    if WC == 'cHl3':
        axs[1].set_ylim([-40., 80.])
    # xlims
    axs[0].set_xlim([inds_bot[0]-0.5, inds_bot[-1]+0.5])
    axs[1].set_xlim([inds_bot[0]-0.5, inds_bot[-1]+0.5])
    # labels
    axs[1].set_xlabel('Analysis Channel SR')
    axs[0].set_ylabel('Events')
    WC_l = WC_pretty_print_dict[WC]
    axs[0].set_title('VVV Yield Summary for '+rf'{WC_l}'+'\n\n')
    axs[2].set_title('Combined Limit')
    axs[1].set_ylabel(ylabel, labelpad=-5.0)
    # set tick labels by bin labels
    axs[0].set_xticks(bin_edges)
    axs[0].set_xticklabels([])
    axs[1].set_xticks(bin_edges_bot)
    axs[1].set_xticklabels(xticklabels_bot, rotation=70)
    # center vertically on the end of the bin label
    for tick in axs[1].xaxis.get_majorticklabels():
        tick.set_horizontalalignment("right")
        tick.set_verticalalignment("top")
    # combined
    axs[2].minorticks_on()
    axs[2].tick_params(axis='x', which='minor', bottom=False)
    axs[2].set_xticks([bin_edges_bot[-2], bin_edges_bot[-1]])
    axs[2].set_xticklabels(['', ''], rotation=0)
    # center vertically on the end of the bin label
    for tick in axs[2].xaxis.get_majorticklabels():
        tick.set_horizontalalignment("center")
        tick.set_verticalalignment("top")
    # inset box
    patches, connectors = axs[1].indicate_inset(bounds=(bin_edges_bot[-2], -3*max_l, 1, 6*max_l), inset_ax=axs[2], edgecolor='black', zorder=11)
    connectors[0].set(visible=True)
    connectors[1].set(visible=True)
    connectors[2].set(visible=False)
    connectors[3].set(visible=False)
    # legends
    axs[0].legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    axs[1].legend(loc='upper left', bbox_to_anchor=(1.0, 0.25))
    # log?
    if logy:
        axs[0].set_yscale('log')
    # save?
    if not savefile is None:
        fig.savefig(savefile+'.pdf')
        fig.savefig(savefile+'.png')

    return fig, axs, df_yields


if __name__=='__main__':
    NTOYS=200
    Unblind=True
    #WCs = ['cW']
    #WCs = WC_ALL

    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default), ...]')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'cW'
    if args.WC == 'all':
        WCs = WC_ALL
    else:
        WCs = [args.WC]

    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    plot_dir = os.path.join(dcdir, 'AN_plots', 'full_analysis', 'freeze', '')

    for WC in WCs:
        print(f'{WC}: ', end='\n')
        #tablepkl = os.path.join(tabledir, f'yiel_table_{WC}.csv')
        #tablepkl = os.path.join(tabledir, f'yield_table_{WC}.pkl')
        tablepkl = os.path.join(tabledir, f'{WC}_summary_df_NTOYS_{NTOYS}.pkl')
        #for channel_rank, ch_str in zip([False, True], ['_by_bin', '_by_channel']):
        for channel_rank, ch_str in zip([True], ['_by_channel']):
            #for logy, log_str in zip([False, True], ['', '_logy']):
            for logy, log_str in zip([True], ['_logy']):
                print(f'channel_rank={channel_rank} & logy={logy}', end='\n')
                savefile = plot_dir+f'yield_{WC}{ch_str}{log_str}'
                # DEBUG
                #print(f'datacard_dict = {datacard_dict}, type={type(datacard_dict)}')
                _ = bin_ranked_yield_histo_bkg_combined(tablepkl, WC, datacard_dict, versions_dict, logy=logy, channel_rank=channel_rank, limit_rank=True, sm_significance=False, savefile=savefile, NTOYS=NTOYS, Unblind=Unblind)
                #_ = bin_ranked_yield_histo_bkg_combined(tablepkl, WC, datacard_dict, logy=logy, channel_rank=channel_rank, limit_rank=False, sm_significance=False, savefile=savefile)
                #fig, axs, df_yields = _
        print()
