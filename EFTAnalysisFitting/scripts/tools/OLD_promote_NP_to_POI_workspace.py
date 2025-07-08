import os
import ROOT
fpath = os.path.dirname(os.path.realpath(__file__))

# Open original workspace file
fin = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'workspaces', 'full_analysis')), '')
fin += 'VVV.all_combined.dim8_All.workspace.vCONFIG_VERSIONS.root'
print(fin)
f_in = ROOT.TFile.Open(fin, "UPDATE")
w = f_in.Get("w")  # or whatever your workspace is named

# Access ModelConfig
mc = w.obj("ModelConfig")

# Get the current POI and nuisance sets
pois = mc.GetParametersOfInterest()
nuis = mc.GetNuisanceParameters()

# Make clones so we can modify
pois = pois.clone("new_poi")
nuis = nuis.clone("new_nuis")

# Promote PDF_ from nuisance to POI
pdf_var = w.var("PDF_")
if not pdf_var:
    print("ERROR: PDF_ not found in workspace")
else:
    # if nuis.contains(pdf_var):
    nuis.remove(pdf_var)
    # if not pois.contains(pdf_var):
    pois.add(pdf_var)

    mc.SetParametersOfInterest(pois)
    mc.SetNuisanceParameters(nuis)
    print("Done. PDF_ promoted to POI")

# Write changes back
w.Write("", ROOT.TObject.kOverwrite)
f_in.Close()
