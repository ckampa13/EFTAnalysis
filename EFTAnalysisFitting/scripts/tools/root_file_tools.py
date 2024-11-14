import ROOT

def book_and_set_TH1D(root_out, hist_name, bin_contents, bin_edges, bin_errors=None, TH1_type='TH1D'):
    # print('hist_name=', hist_name)
    nbins = len(bin_contents)
    if TH1_type == 'TH1D':
        h1d = ROOT.TH1D(hist_name, '', nbins, bin_edges)
        # don't add to registry
        h1d.SetDirectory(0)
    elif TH1_type == 'TH1F':
        h1d = ROOT.TH1F(hist_name, '', nbins, bin_edges)
        # don't add to registry
        h1d.SetDirectory(0)
    else:
        raise ValueError('TH1_type = "%s" is not allowed. Select between ["TH1D", "TH1F"].' % TH1_type)
    # set bin contents
    for i in range(nbins):
        h1d.SetBinContent(i+1, bin_contents[i])
    # set bin errors if they are passed in
    if not bin_errors is None:
        for i in range(nbins):
            h1d.SetBinError(i+1, bin_errors[i])
    root_out.WriteObject(h1d, hist_name)


def book_and_set_TH2D(root_out, hist_name, bin_contents_2D, bin_edges_x, bin_edges_y, bin_errors_2D=None, TH2_type='TH2D'):
    # print('hist_name=', hist_name)
    nbins_x = bin_contents_2D.shape[0]
    nbins_y = bin_contents_2D.shape[1]
    if TH2_type == 'TH2D':
        h2d = ROOT.TH2D(hist_name, '', nbins_x, bin_edges_x, nbins_y, bin_edges_y)
        # don't add to registry
        h2d.SetDirectory(0)
    elif TH2_type == 'TH2F':
        h2d = ROOT.TH2F(hist_name, '', nbins_x, bin_edges_x, nbins_y, bin_edges_y)
        # don't add to registry
        h2d.SetDirectory(0)
    else:
        raise ValueError('TH2_type = "%s" is not allowed. Select between ["TH2D", "TH2F"].' % TH2_type)
    # set bin contents
    for i in range(nbins_x):
        for j in range(nbins_y):
            h2d.SetBinContent(i+1, j+1, bin_contents_2D[i, j])
    # set bin errors if they are passed in
    if not bin_errors_2D is None:
        for i in range(nbins_x):
            for j in range(nbins_y):
                h2d.SetBinError(i+1, j+1, bin_errors_2D[i, j])
    root_out.WriteObject(h2d, hist_name)
