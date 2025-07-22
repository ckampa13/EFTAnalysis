import os
import sys
fpath = os.path.dirname(os.path.realpath(__file__))

def template_vals_list_to_tex(vals):
    str_list = []
    for v in vals:
        nums = v.split('=')[1]
        c = nums.split('+')[0]
        unc = nums.split('+')[1]
        u = unc.split('-')[0]
        d = unc.split('-')[1]
        str_list.append(rf'${c}^{{+{u}}}_{{-{d}}}$')
    return str_list

def parse_template_fit_values(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    template_fit_dict = {'best_fit': {}}
    for line in lines:
        if 'mVVV_bin_centers' in line:
            bin_centers = line.rstrip().replace('mVVV_bin_centers = [','').replace(']','').split(', ')
            template_fit_dict['bin_centers'] = bin_centers
        if 'mVVV_bin_edges' in line:
            bin_edges = line.rstrip().replace('mVVV_bin_edges = [','').replace(']','').split(', ')
            # clean edges to make sure they are ints
            bin_edges = [str(int(float(b))) for b in bin_edges]
            template_fit_dict['bin_edges'] = bin_edges
        if "cW" in line or "cHq3" in line or "Asimov" in line or "Data" in line:
            dict_label = line.split(' ')[0].rstrip().replace(':', '')
            print(dict_label)
        if 'Best fit:' in line:
            vals = line.replace('Best fit: ', '').rstrip().replace('[','').replace(']','').split(', ')
            str_list = template_vals_list_to_tex(vals)
            template_fit_dict['best_fit'][dict_label] = {'vals': vals, 'tex_list': str_list}
    return template_fit_dict

def make_tex_table(template_fit_dict, fit_order, tex_file=None):
    # Construct the LaTeX table as a string
    table = r"\begin{table}[hbtp!]" + "\n"
    table += r"\centering" + "\n"
    # caption
    table += r"\topcaption{\label{tab:templatefit}" + "\n"
    table += r"Summary of the fitted multiplicative values in the template fit" + "\n"
    table += "}\n"
    #table += r"\renewcommand{\arraystretch}[1.3]" + "\n"
    table += r"\renewcommand{\arraystretch}{1.3}" + "\n"
    bf = template_fit_dict['best_fit']
    N_fits = len(bf)
    N_exp = N_fits - 1 # only 1 data, in the last column
    begin_str = r"\begin{tabular}{r"
    for i in range(N_fits):
        if i == N_fits -1:
            begin_str += "r"
        else:
            begin_str += "c"
    begin_str += "}\n"
    table += begin_str
    table += r"\hline" + "\n"
    # header
    header_str = r"\mVVV bin& \multicolumn{" + str(N_exp) + r"}{c}{expected} & measured \\" + "\n"
    header_str += r"$[$GeV$]$ & "
    for i, fit_name in enumerate(fit_order[:-1]): # don't include Data
        if i == N_fits - 2:
            tail = r"& \\" + "\n"
        else:
            tail = r"&"
        if 'cW' in fit_name:
            val = int(float(fit_name.split('_')[1].replace('m', '-').replace('p', '.')))
            header_str += r" $\cW =" + str(val) + r"\TeV^{-2}$ "
        elif 'cHq3' in fit_name:
            val = int(float(fit_name.split('_')[1].replace('m', '-').replace('p', '.')))
            header_str += r" $\cHqthree =" + str(val) + r"\TeV^{-2}$ "
        else: # Asimov
            header_str += r" SM "
        header_str += tail
    table += header_str
    table += r"\hline" + "\n"
    # loop through rows
    N_bins = len(bf['Data']['vals'])
    be = template_fit_dict['bin_edges']
    for i in range(N_bins):
        row_str = ''
        le = be[i]
        ue = be[i+1]
        if i == N_bins - 1:
            ue = r"~~~$\infty$"
        row_str += le + ' -- ' + ue + ' &'
        for j, fit_name in enumerate(fit_order): # include Data
            if j == N_fits - 1:
                tail = r"\\" + "\n"
            else:
                tail = r"&"
            tex = bf[fit_name]['tex_list']
            row_str += " " + tex[i] + " " + tail
        table += row_str
    # close table
    table += r"\hline" + "\n"
    table += r"\end{tabular}" + "\n"
    table += r"\end{table}" + "\n"

    print(table)

    if not tex_file is None:
        with open(tex_file, 'w') as f:
            f.write(table)
    return table

if __name__=='__main__':
    ddir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'AN_plots', 'aux')), '')
    plotdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'AN_plots', 'tables')), '')
    # files
    input_file = ddir+'template_fit_numerical_vals.txt'
    tex_file = plotdir+f'templatefit.tex'
    template_fit_dict = parse_template_fit_values(input_file)
    # update if we change fits or order
    fit_order = ['cW_1p0', 'cHq3_1p0', 'Asimov', 'Data']
    make_tex_table(template_fit_dict, fit_order, tex_file)
