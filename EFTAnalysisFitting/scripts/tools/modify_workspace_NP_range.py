import os
import ROOT
fpath = os.path.dirname(os.path.realpath(__file__))

# Open original workspace file
fin = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'workspaces', 'full_analysis')), '')
fin += 'VVV.all_combined.dim8_All.workspace.vCONFIG_VERSIONS.root'
print(fin)
f_in = ROOT.TFile.Open(fin, "UPDATE")
w = f_in.Get("w")  # or whatever your workspace is named

# Modify parameter range
params = {'PDF_': [-1.0, 1.0]}
for p, r in params.items():
    for suff in ['', '_In']:
        param = w.var(p+suff)
        if param:
            param.setRange(r[0], r[1])
            print("Set range for %s to [%.1f, %.1f]" % (param.GetName(), r[0], r[1]))
        else:
            print("Parameter %s not found!" % p+suff)

# Optionally: save workspace again (overwrite original)
w.Write("", ROOT.TObject.kOverwrite)
f_in.Close()

