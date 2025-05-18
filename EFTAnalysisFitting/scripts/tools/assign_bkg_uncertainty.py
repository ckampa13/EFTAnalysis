import numpy as np

def get_bkg_procs_and_systs(keys):
    # ignores sm, which is treated differently from other bkgs
    bkgs = set()
    bkgs_Up = set()
    for k in keys:
        if not 'VVV' in k and not 'Up' in k and not 'Down' in k and not 'quad' in k and not 'lin' in k and not 'sm' in k and not 'data' in k:
            bkgs.add(k)
    bkgs = list(bkgs)
    bkg_systs_dict = {b: None for b in bkgs}
    for bkg in bkgs:
        for k in keys:
            if bkg in k and 'Up' in k and not 'VVV' in k and not 'quad' in k and not 'lin' in k and not 'sm' in k:
                bkg_systs_dict[bkg] = k
                break
    return bkg_systs_dict

def create_bkg_Up_Down_templates(root_in, nominal_name, Up_name, Down_name, bkg_assigned_dict_ch):
    bkg = nominal_name.replace('h_', '')
    a_vals = bkg_assigned_dict_ch[bkg]
    hin = root_in.Get(nominal_name)
    nbins = hin.GetNbinsX()
    nom_vals = [hin.GetBinContent(i+1) for i in range(nbins)]
    hin = root_in.Get(Up_name)
    Up_vals_in = [hin.GetBinContent(i+1) for i in range(nbins)]
    hin = root_in.Get(Down_name)
    Down_vals_in = [hin.GetBinContent(i+1) for i in range(nbins)]
    Up_vals = []
    Down_vals = []
    for i in range(nbins):
        a = a_vals[i]
        nv = nom_vals[i]
        if np.isclose(a, -200): # use original from file ("total" column)
            Up_vals.append(Up_vals_in[i])
            Down_vals.append(Down_vals_in[i])
        elif np.isclose(a, -100): # use nominal
            Up_vals.append(nv)
            Down_vals.append(nv)
        else:
            # calulate based on assigned uncertainty (percentage)
            uval = (1. + a) * nv
            dval = (1. - a) * nv
            Up_vals.append(uval)
            Down_vals.append(dval)
    return np.array(nom_vals), np.array(Up_vals), np.array(Down_vals), np.array(Up_vals_in), np.array(Down_vals_in)
