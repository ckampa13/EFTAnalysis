import ROOT

def book_and_set_TH1D(root_out, hist_name, bin_contents, bin_edges, bin_errors=None):
    nbins = len(bin_contents)
    h1d = ROOT.TH1D(hist_name, '', nbins, bin_edges)
    # set bin contents
    for i in range(nbins):
        h1d.SetBinContent(i+1, bin_contents[i])
    # set bin errors if they are passed in
    if not bin_errors is None:
        for i in range(nbins):
            h1d.SetBinError(i+1, bin_errors[i])
    root_out.WriteObject(h1d, hist_name)
