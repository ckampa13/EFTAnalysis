# this runs with python 2 (needs pyROOT)
import os
import numpy as np
# import lmfit as lm # lmfit not in python2
import ROOT
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from MISC_CONFIGS import dim6_ops

# c0 + c1 * x + c2 * x**2
def quad_mod(x, **params):
    return params['c0'] + params['c1']*x + params['c2']*x**2

def get_new_param_dict(params):
    lambda_ = params['c2']
    alpha_ = -params['c1']/(2*params['c2'])
    gamma_ = params['c0'] - params['c1']**2 / (4*params['c2'])
    return {'lambda': lambda_, 'alpha': alpha_, 'gamma': gamma_}

def construct_EFT_terms_WC(WC, file_root, VVV='VVV'):
    x_vals = []
    y_vals_bins = []
    keys_cleaned = [k.GetName().split(';')[0] for k in file_root.GetListOfKeys() if "TH1" in k.GetClassName()]
    nbins = file_root.Get(keys_cleaned[0]).GetNbinsX()
    for k in keys_cleaned:
        #if f'_{WC}_' in k and "p" in k.split('_')[3]:
        # FIXME! kludge for Philip FT0 development
        # But it does work, so maybe leave it
        try:
            k3 = k.split('_')[3]
        except:
            k3 = 'FAIL'
        try:
            k3_ = int(k3)
            k3_is_int = True
        except:
            k3_is_int = False
        if ('_'+WC+'_' in k) and (VVV in k) and (("p" in k3) or ("m" in k3) or (k3_is_int)):
            # avoid systematics
            if (not "Up" in k) and (not "Down" in k):
                x_val = float(k.split('_')[-1].split(';')[0].replace('m', '-').replace('p','.'))
                x_vals.append(x_val)
                hin = file_root.Get(k)
                y_vals = np.array([hin.GetBinContent(i+1) for i in range(nbins)])
                y_vals_bins.append(y_vals)
    x_vals = np.array(x_vals)
    y_vals_bins = np.array(y_vals_bins).T
    # using lmfit (contains e.g. chi2)
    # results = []
    for y_vals in y_vals_bins:
        '''
        # lmfit model
        model = lm.Model(quad_mod, independent_vars=['x'])
        params = lm.Parameters()
        params.add('c0', value=0)
        params.add('c1', value=0)
        params.add('c2', value=0)
        # fit
        result = model.fit(y_vals, x=x_vals, params=params)
        results.append(result)
        '''
    # use numpy only? -- can probably remove this
    results_np = []
    for y_vals in y_vals_bins:
        c2, c1, c0 = np.polyfit(x_vals, y_vals, deg=2)
        yfit = np.polyval((c2, c1, c0), x_vals)
        chi2 = np.sum((yfit - y_vals)**2)
        redchi = chi2 / (len(x_vals) - 3)
        results_np.append({'params': {'c0': c0, 'c1': c1, 'c2': c2}, 'chi2': chi2, 'redchi': redchi})
    #return results, results_np, x_vals, y_vals_bins
    return results_np, x_vals, y_vals_bins

def construct_EFT_terms_all(WCs, filename, rchi2_cut=0.1, verbose=True):
    print('Now fitting EFT point scans...')
    #results_dict = {}
    results_np_dict = {}
    x_vals_dict = {}
    y_vals_bins_dict = {}
    #with uproot.open(filename) as file_:
    file_ = ROOT.TFile(filename, 'read')
    for WC in WCs:
        #results, results_np, x_vals, y_vals_bins = construct_EFT_terms_WC(WC, file_)
        #results_dict[WC] = results
        results_np, x_vals, y_vals_bins = construct_EFT_terms_WC(WC, file_)
        results_np_dict[WC] = results_np
        x_vals_dict[WC] = x_vals
        y_vals_bins_dict[WC] = y_vals_bins
    file_.Close()
    # print the redchi2
    above_rchi = []
    above_vals = []
    strsm_ = ''
    print('reducedchi2 values:')
    for WC, results in results_np_dict.items():
        str_ = WC+': '
        strsm_ += WC+': ['
        for i, result in enumerate(results):
            bin_n = i + 1
            redchi = result['redchi']
            if redchi > rchi2_cut:
                above_rchi.append(WC+'_bin'+str(bin_n))
                above_vals.append(redchi)
            str_ += str(bin_n) + ' rchi2 = ' + ('%0.2E' % redchi) + ', '
            strsm_ += '%0.3f' % result['params']['c0'] + ','
        str_ += '\n'
        strsm_ += ']\n'
        if verbose:
            print(str_)
        # print()
    strsm_ += '\n'
    # print any cases that are above cutoff
    print('Found %d bins with large redchi2 (>%0.2E):' % (len(above_rchi), rchi2_cut))
    str_ = ''
    for k, v in zip(above_rchi, above_vals):
        str_ += k + ': ' + ('%0.2E' % v) + ', '
    str_ += '\n'
    print(str_)
    if verbose:
        # find which SM values we will use, and tell the user
        dim8 = "n/a"
        for WC in WCs:
            if WC in dim6_ops:
                dim6 = WC
                break
        for WC in WCs:
            if not WC in dim6_ops:
                dim8 = WC
                break
        print('SM values from fits (dim6 should match, dim8 should match):')
        print(strsm_)
        print('dim6 SM will be %s fit values' % dim6)
        print('dim8 SM will be %s fit values' % dim8)
    #return results_dict, results_np_dict, x_vals_dict, y_vals_bins_dict
    return results_np_dict, x_vals_dict, y_vals_bins_dict
