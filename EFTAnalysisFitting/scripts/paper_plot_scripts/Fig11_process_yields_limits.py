import os
import argparse
import sys
from copy import deepcopy
from collections.abc import Iterable
import math
import numpy as np
import pickle as pkl
import pandas as pd
import uproot
import ROOT
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs
from MISC_CONFIGS import (
    datacard_dir,
    template_filename_yields,
    template_outfilename,
    template_fitDiagfilename,
    bkgs_all,
    #template_outfilename_stub,
    dim6_ops,
    #WC_pretty_print_dict,
    WC_pretty_print_dict_AN,
    SR_pretty_print_dict_AN,
)
from tools.extract_limits_multi_interval import get_lims_w_best, get_lims_quad_interp

def process_yields_limits(WC, datacard_dict, versions_dict, NTOYS=200, Unblind=True, use_fit='fit_b'):
    CL_list = [0.95]
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    output_dir_bin = os.path.join(dcdir, 'output', 'single_bin')
    output_dir_sch = os.path.join(dcdir, 'output', 'subchannel')
    output_dir_full = os.path.join(dcdir, 'output', 'full_analysis')
    # FitDiag file for pre-fit and post-fit yields
    root_filename = os.path.join(output_dir_full, template_fitDiagfilename.substitute(asimov='Data', NTOYS=NTOYS))
    file_ur = uproot.open(root_filename)
    # file_ROOT = ROOT.TFile(root_filename, 'READ')
    # fit_s = file_ROOT.Get('fit_s')
    # param = fit_s.floatParsFinal().find(f'k_{WC}')
    # WC_best_fit_d = param.getVal()
    # full analysis limits
    fname_a = template_outfilename.substitute(asimov='Asimov', channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version='vCONFIG_VERSIONS', syst='syst', method='MultiDimFit')
    fname_a = os.path.join(output_dir_full, fname_a)
    fname_d = template_outfilename.substitute(asimov='Data', channel='all', subchannel='_combined', WC=WC, ScanType='_1D',version='vCONFIG_VERSIONS', syst='syst', method='MultiDimFit')
    fname_d = os.path.join(output_dir_full, fname_d)
    _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_a, WC=WC, extrapolate=True)
    Cs_f_a, NLL_f_a, CL_list_f_a, NLL_cuts_f_a, LLs_f_a, ULs_f_a, LLs_interp_f_a, ULs_interp_f_a, C_best_f_a, NLL_best_f_a = _
    _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True)
    Cs_f_d, NLL_f_d, CL_list_f_d, NLL_cuts_f_d, LLs_f_d, ULs_f_d, LLs_interp_f_d, ULs_interp_f_d, C_best_f_d, NLL_best_f_d = _
    # best fit
    WC_best_fit_d = C_best_f_d
    WC_best_fit_a = C_best_f_a
    # DEBUG
    print(f'Best fit {WC}: {WC_best_fit_a:0.4f} (Asimov), {WC_best_fit_d:0.4f} (Data)')
    # pick the widest range of the limit
    # FIXME! Allow multi-intervals?
    LL_f_a = np.min(LLs_interp_f_a[0])
    UL_f_a = np.max(ULs_interp_f_a[0])
    LL_f_d = np.min(LLs_interp_f_d[0])
    UL_f_d = np.max(ULs_interp_f_d[0])
    # load the original yield files -- need SM for prefit
    # also load bins
    bins_dict = {}
    ##file_urs_input = {}
    output_list = []
    print('Making yield summary dataframe...')
    for ch, d_ch in datacard_dict.items():
        v = versions_dict[ch]['v']
        version = f'v{v}'
        fname_ch = d_ch['info']['short_name']
        for sch, d_sch in d_ch['subchannels'].items():
            print(f'Channel: {ch}, Subchannel: {sch}')
            sch_dict = {}
            fname_sch = d_sch['info']['short_name']
            # combined limit (subch)
            fname_a = template_outfilename.substitute(asimov='Asimov', channel=fname_ch, subchannel=fname_sch, WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
            fname_a = os.path.join(output_dir_sch, fname_a)
            fname_d = template_outfilename.substitute(asimov='Data', channel=fname_ch, subchannel=fname_sch, WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
            fname_d = os.path.join(output_dir_sch, fname_d)
            _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_a, WC=WC, extrapolate=True)
            Cs_s_a, NLL_s_a, CL_list_s_a, NLL_cuts_s_a, LLs_s_a, ULs_s_a, LLs_interp_s_a, ULs_interp_s_a, C_best_s_a, NLL_best_s_a = _
            _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname_d, WC=WC, extrapolate=True)
            Cs_s_d, NLL_s_d, CL_list_s_d, NLL_cuts_s_d, LLs_s_d, ULs_s_d, LLs_interp_s_d, ULs_interp_s_d, C_best_s_d, NLL_best_s_d = _
            # pick the widest range of the limit
            # FIXME! Allow multi-intervals?
            LL_s_a = np.min(LLs_interp_s_a[0])
            UL_s_a = np.max(ULs_interp_s_a[0])
            LL_s_d = np.min(LLs_interp_s_d[0])
            UL_s_d = np.max(ULs_interp_s_d[0])
            # yields
            if WC in dim6_WCs:
                suff_proc = ''
            else:
                suff_proc = '_dim8'
            fname_yield = template_filename_yields.substitute(channel=fname_ch, subchannel=fname_sch,
                                                      purpose='DataCard_Yields', proc='_MultiDimCleaned'+suff_proc, version=version, file_type='root')
            ddir_base = os.path.join(dcdir, ch, version)
            fname_yield = os.path.join(ddir_base, fname_yield)
            file_ur_ = uproot.open(fname_yield)
            # get info on the EFTs
            sm_vals = file_ur_['h_sm'].values()
            quad_vals = file_ur_[f'h_quad_{WC}'].values()
            sm_lin_quad_vals = file_ur_[f'h_sm_lin_quad_{WC}'].values()
            lin_vals = sm_lin_quad_vals - sm_vals - quad_vals
            yield_EFT = lambda x : sm_vals + lin_vals*x + quad_vals*x**2
            UL_yield_WC_at_lim_f_a = yield_EFT(UL_f_a)
            UL_yield_WC_at_lim_s_a = yield_EFT(UL_s_a)
            UL_yield_WC_at_lim_f_d = yield_EFT(UL_f_d)
            UL_yield_WC_at_lim_s_d = yield_EFT(UL_s_d)
            LL_yield_WC_at_lim_f_a = yield_EFT(LL_f_a)
            LL_yield_WC_at_lim_s_a = yield_EFT(LL_s_a)
            LL_yield_WC_at_lim_f_d = yield_EFT(LL_f_d)
            LL_yield_WC_at_lim_s_d = yield_EFT(LL_s_d)
            yield_WC_0p3 = yield_EFT(0.3)
            yield_WC_1 = yield_EFT(1.0)
            # sm for the stack
            sm_prefit = deepcopy(file_ur_['h_sm'].values())
            sm_err_prefit = deepcopy(file_ur_['h_sm'].errors())
            nbins = len(sm_prefit)
            #err_sm = deepcopy(file_ur_['h_sm'].errors()) # I don't think I need this
            #file_urs_input[fname_ch+'sch'+fname_sch] = file_ur_
            bin_edges = deepcopy(file_ur_['h_sm'].to_numpy()[1])
            # special cases?
            if ch == '2Lepton_OS_2FJ':
                bin_edges[-1] = 5000. # originally set to 10000. but this is just overflow
            bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
            subch_key = fname_ch+'sch'+fname_sch
            bins_dict[subch_key] = {'bin_edges': bin_edges, 'bin_centers': bin_centers, 'sm': sm_prefit}
            # sm postfit
            sm_postfit = deepcopy(file_ur[f'shapes_{use_fit}']['ch'+subch_key]['sm'].values()[:nbins])
            # data
            data = file_ur['shapes_prefit']['ch'+subch_key]['data'].values()[1]
            #data_err = np.sqrt(data)
            data_err_D = file_ur['shapes_prefit']['ch'+subch_key]['data'].errors(which='low')[1]
            data_err_U = file_ur['shapes_prefit']['ch'+subch_key]['data'].errors(which='high')[1]
            # DEBUG
            # print(f'data_err_D, data_err_U = {data_err_D}, {data_err_U}')
            # update subch dict
            sch_dict['channel'] = ch
            sch_dict['subchannel'] = sch
            #sch_dict[f'yield_sm_prefit'] = sm_prefit
            #sch_dict[f'yield_sm_postfit'] = sm_postfit
            sch_dict[f'{WC}_best_fit_Asimov'] = WC_best_fit_a
            sch_dict[f'{WC}_best_fit_Data'] = WC_best_fit_d
            sch_dict[f'comb_{WC}_95CL_LL_Asimov'] = LL_s_a
            sch_dict[f'comb_{WC}_95CL_UL_Asimov'] = UL_s_a
            sch_dict[f'all_comb_{WC}_95CL_LL_Asimov'] = LL_f_a
            sch_dict[f'all_comb_{WC}_95CL_UL_Asimov'] = UL_f_a
            sch_dict[f'comb_{WC}_95CL_LL_Data'] = LL_s_d
            sch_dict[f'comb_{WC}_95CL_UL_Data'] = UL_s_d
            sch_dict[f'all_comb_{WC}_95CL_LL_Data'] = LL_f_d
            sch_dict[f'all_comb_{WC}_95CL_UL_Data'] = UL_f_d
            # loop through bins
            for i in range(len(bin_centers)):
                bin_dict = {}
                bin_ = i + 1
                bin_dict['bin'] = bin_
                bin_dict['bin_low'] = bins_dict[subch_key]['bin_edges'][0]
                bin_dict['bin_high'] = bins_dict[subch_key]['bin_edges'][1]
                bin_dict['data'] = data[i]
                bin_dict['data_err_D'] = data_err_D[i]
                bin_dict['data_err_U'] = data_err_U[i]
                bin_dict[f'yield_sm_prefit'] = sm_prefit[i]
                bin_dict[f'yield_sm_postfit'] = sm_postfit[i]
                bin_dict[f'comb_yield_{WC}_95CL_LL_Asimov'] = LL_yield_WC_at_lim_s_a[i]
                bin_dict[f'comb_yield_{WC}_95CL_UL_Asimov'] = UL_yield_WC_at_lim_s_a[i]
                bin_dict[f'comb_yield_{WC}_95CL_LL_Data'] = LL_yield_WC_at_lim_s_d[i]
                bin_dict[f'comb_yield_{WC}_95CL_UL_Data'] = UL_yield_WC_at_lim_s_d[i]
                bin_dict[f'all_comb_yield_{WC}_95CL_LL_Asimov'] = LL_yield_WC_at_lim_f_a[i]
                bin_dict[f'all_comb_yield_{WC}_95CL_UL_Asimov'] = UL_yield_WC_at_lim_f_a[i]
                bin_dict[f'all_comb_yield_{WC}_95CL_LL_Data'] = LL_yield_WC_at_lim_f_d[i]
                bin_dict[f'all_comb_yield_{WC}_95CL_UL_Data'] = UL_yield_WC_at_lim_f_d[i]
                bin_dict[f'yield_{WC}_at_0p3'] = yield_WC_0p3[i]
                bin_dict[f'yield_{WC}_at_1'] = yield_WC_1[i]
                bin_dict[f'sm_{WC}'] = sm_vals[i]
                bin_dict[f'quad_{WC}'] = quad_vals[i]
                bin_dict[f'sm_lin_quad_{WC}'] = sm_lin_quad_vals[i]
                bin_dict[f'lin_{WC}'] = lin_vals[i]
                fname_sch_b = fname_sch + f'_bin{bin_}'
                # get limits
                # loop through data and asimov
                for asi_str in ['Asimov', 'Data']:
                    fname = template_outfilename.substitute(asimov=asi_str, channel=fname_ch, subchannel=fname_sch_b, WC=WC, ScanType='_1D',version=version, syst='syst', method='MultiDimFit')
                    fname = os.path.join(output_dir_bin, fname)
                    _ = get_lims_w_best(CL_list, Cs=None, NLL=None, root_file=fname, WC=WC, extrapolate=True)
                    Cs, NLL, CL_list, NLL_cuts, LLs, ULs, LLs_interp, ULs_interp, C_best, NLL_best = _
                    # pick the widest range of the limit
                    # FIXME! Allow multi-intervals?
                    LL_ = np.min(LLs_interp[0])
                    UL_ = np.max(ULs_interp[0])
                    LL_yield_b = yield_EFT(LL_)[i]
                    UL_yield_b = yield_EFT(UL_)[i]
                    # add to dict
                    bin_dict[f'{WC}_95CL_UL_{asi_str}'] = UL_
                    bin_dict[f'{WC}_95CL_LL_{asi_str}'] = LL_
                    bin_dict[f'yield_{WC}_95CL_UL_{asi_str}'] = UL_yield_b
                    bin_dict[f'yield_{WC}_95CL_LL_{asi_str}'] = LL_yield_b
                # add the subch information
                bin_dict.update(deepcopy(sch_dict))
                # loop through bkgs
                #totals = {'prefit': 0., 'postfit': 0.}
                #total_err2s = {'prefit': 0., 'postfit': 0.}
                for proc in bkgs_all:
                    keys = [k.split(';')[0] for k in file_ur['shapes_prefit']['ch'+subch_key]]
                    if not proc in keys:
                        continue
                    proc_dict = {'process': proc}
                    # loop through pre-fit and post-fit to add bkgs
                    for fit, fit_name in zip(['prefit', 'postfit'], ['shapes_prefit', f'shapes_{use_fit}']):
                        # shapes
                        shapes = file_ur[fit_name]['ch'+subch_key]
                        n_ = deepcopy(shapes[proc].values()[:len(bin_centers)])[i]
                        n_err_ = deepcopy(shapes[proc].errors()[:len(bin_centers)])[i]
                        #totals[fit] += n_
                        #total_err2s[fit] += n_err_**2
                        # DEBUG
                        # if isinstance(n_, Iterable):
                        #     print(f'n_ is iterable! {ch}, {sch}, {proc}, {fit_name}')
                        #     print(n_)
                        proc_dict[f'yield_{fit}'] = n_
                        proc_dict[f'yield_err_{fit}'] = n_err_
                    # update with bin dict
                    proc_dict.update(deepcopy(bin_dict))
                    # add to list
                    output_list.append(proc_dict)
                # add SM
                proc_dict = {'process': 'sm', 'yield_prefit': sm_prefit[i], 'yield_err_prefit': sm_err_prefit[i]}
                shapes = file_ur[f'shapes_{use_fit}']['ch'+subch_key]
                n_ = deepcopy(shapes['sm'].values()[:len(bin_centers)])[i]
                n_err_ = deepcopy(shapes['sm'].errors()[:len(bin_centers)])[i]
                # DEBUG
                # if isinstance(n_, Iterable):
                #     print(f'n_ is iterable! {ch}, {sch}, sm')
                #     print(n_)
                proc_dict[f'yield_{fit}'] = n_
                proc_dict[f'yield_err_{fit}'] = n_err_
                # update with bin dict
                proc_dict.update(deepcopy(bin_dict))
                # add to list
                output_list.append(proc_dict)
    df = pd.DataFrame(output_list)
    #print(df)
    # total bg and uncertainties
    df.loc[:, 'channel_subchannel'] = [f'{ch}_{sch}' for ch, sch in zip(df.channel.values, df.subchannel.values)]
    for j, ch_sch in enumerate(df.channel_subchannel.unique()):
        for i, bin_ in enumerate(df.bin.unique()):
            m = ((df['bin'] == bin_) & (df['channel_subchannel'] == ch_sch))
            for fit in ['prefit', 'postfit']:
                # print(df.loc[m, f'yield_{fit}'])
                df.loc[m, f'total_bkg_{fit}'] = df.loc[m, f'yield_{fit}'].values.sum()
                df.loc[m, f'total_bkg_err_{fit}'] = ((df.loc[m, f'yield_err_{fit}']**2).values.sum())**(1/2)
    # close ROOT file and return
    #file_ROOT.Close()
    print('Done.\n')
    return df


if __name__=='__main__':
    Unblind=True
    #WC = 'cW'
    NTOYS = 200

    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help=f'Which Wilson Coefficient to study for 1D limits? ["cW" (default), "cHl3", ...]')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'cW'
    if args.WC == 'all':
        WCs = WC_ALL
    else:
        WCs = [args.WC]

    for WC in WCs:
        print(f'{WC}')
        df = process_yields_limits(WC, datacard_dict, versions_dict, NTOYS=NTOYS, Unblind=Unblind)
        # save to output
        dcdir = datacard_dir
        if Unblind:
            dcdir = os.path.join(dcdir, 'unblind')
        output_dir = os.path.join(dcdir, 'paper_plots', 'Fig11')
        output_file = os.path.join(output_dir, f'Fig11_{WC}_summary_df_NTOYS_{NTOYS}.pkl')
        df.to_pickle(output_file)
        print(df)
