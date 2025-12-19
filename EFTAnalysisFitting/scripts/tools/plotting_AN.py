import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator
from datetime import datetime
from decimal import localcontext, Decimal, ROUND_HALF_UP

FONTSIZE=28.0
LABELSIZE=34.0

# # Helvetica == TeX Gyre Heros
# family = 'TeX Gyre Heros'
# # add any relevant fonts (with bold and italics) to
# for f in font_manager.findSystemFonts(fontext='ttf'):
#     if 'texgyreheros' in f:
#         font_manager.fontManager.addfont(f)

# nicer plot formatting
def config_plots(grid=False):
    # Helvetica == TeX Gyre Heros
    family = 'TeX Gyre Heros'
    # add any relevant fonts (with bold and italics) to
    for f in font_manager.findSystemFonts(fontext='ttf'):
        if 'texgyreheros' in f:
            font_manager.fontManager.addfont(f)

    #must run twice for some reason (glitch in Jupyter)
    for i in range(2):
        plt.rcParams['figure.figsize'] = [10, 8] # larger figures
        #plt.rcParams['axes.grid'] = True         # turn grid lines on
        plt.rcParams['axes.grid'] = grid        # turn grid lines off (CMS convention)
        #plt.rcParams['axes.axisbelow'] = True    # put grid below points
        #plt.rcParams['grid.linestyle'] = '--'    # dashed grid
        plt.rcParams.update({'font.size': FONTSIZE})   # increase plot font size
        #plt.rcParams.update({"text.usetex": True})
        #plt.rcParams.update({"text.usetex": False})
        # to pretty print WC need these lines
        plt.rc("text", usetex=True)
        # plt.rc("text", usetex=False)
        #plt.rc("text.latex", preamble=r"\usepackage{amsmath}\usepackage{amssymb}")
        #plt.rc("text.latex", preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{color}")
        plt.rcParams.update({
            "text.latex.preamble": r"""
\usepackage{tgheros}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{sansmath}
\sansmath
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{color}
\usepackage{upgreek}
"""
        })
        #plt.rc("text.latex", preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{color}\usepackage{tex-gyre-heros}")
        # apply in each file as needed
        #plt.rcParams['figure.constrained_layout.use'] = True
        plt.rc('axes', labelsize=LABELSIZE)     # fontsize of the axes title
        # switch font
        #plt.rc('font', serif=['Times New Roman']) # only use Times New Roman
        #plt.rc('font', family='serif') # switch to serif
        #plt.rc('font', family='Helvetica')
        plt.rcParams.update({
            #"font.family": family,
            "font.family": 'sans-serif',
            #"font.sans-serif": [family, "DejaVu Sans", "Nimbus Sans L", "Arial"],
            "font.sans-serif": [family],
            "mathtext.fontset": "custom",
            "mathtext.rm": family,
            "mathtext.it": f"{family}:italic",
            "mathtext.bf": f"{family}:bold",
        })

def ticks_in(ax, top_and_right=True):
    if top_and_right:
        ax.tick_params(which='both', direction='in', right=True, top=True)
    else:
        ax.tick_params(which='both', direction='in')
    return ax

def ticks_sizes(ax, major={'L':20,'W':2}, minor={'L':10,'W':1}):
    ax.tick_params('both', length=major['L'], width=major['W'], which='major')
    ax.tick_params('both', length=minor['L'], width=minor['W'], which='minor')
    return ax

# label for histogram
def get_label(data, bins):
    over = (data > np.max(bins)).sum()
    under = (data < np.min(bins)).sum()
    data_ = data[(data <= np.max(bins)) & (data >= np.min(bins))]
    mean = f'{np.mean(data_):.3E}'
    std = f'{np.std(data_, ddof=1):.3E}'
    label = f'mean: {mean:>15}\nstddev: {std:>15}\nIntegral: {len(data):>17}\n'\
    +f'Underflow: {under:>16}\nOverflow: {over:>16}'
    return label

# CMS wrapper for title
def CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True, inside_frame=True, xloc=None, yloc=None):
    lefttitle=r'$\bf{CMS}$'
    if prelim:
        #lefttitle += r' $\it{Preliminary}$'
        lefttitle += r' $\text{\sffamily\itshape Preliminary}$'
    righttitle = rf'{lumi} {lumi_unit}$^{{-1}}$ ({energy})'
    if xloc is None:
        xloc = 0.03
    if yloc is None:
        yloc = 0.98
    if inside_frame:
        ax.text(xloc, yloc, lefttitle, transform=ax.transAxes, ha='left', va='top', fontsize=LABELSIZE)
    else:
        # ax.set_title(lefttitle, fontweight ='bold', loc='left')
        ax.set_title(lefttitle, loc='left')
    ax.set_title(righttitle, loc='right')

def numerical_formatter(value_float):
    # check if we should remove the preceding negative
    if abs(np.round(value_float, decimals=3)) < 0.001:
        vf = abs(value_float)
    else:
        vf = value_float
    if abs(vf) < 0.1:
        s = f'{vf:0.3f}'
    elif abs(vf) < 2.0:
        s = f'{vf:0.2f}'
    elif abs(vf) < 10.:
        s = f'{vf:0.1f}'
    else:
        # above 10, round to integer
        # use decimal package to avoid bankers rounding
        # with localcontext() as ctx:
        #     ctx.rounding = ROUND_HALF_UP
        #     dval = Decimal(value_float)
        #     rval = dval.to_integral_value()
        # s = f'{rval}'
        # or just use f-string, which rounds appropriately
        s = f'{vf:0.0f}'
    return s

def numerical_formatter_with_ndec_return(value_float):
    if abs(value_float) < 0.1:
        s = f'{value_float:0.3f}'
        nd = 3
    elif abs(value_float) < 2.0:
        s = f'{value_float:0.2f}'
        nd = 2
    elif abs(value_float) < 10.:
        s = f'{value_float:0.1f}'
        nd = 1
    else:
        # above 10, round to integer
        # use decimal package to avoid bankers rounding
        # with localcontext() as ctx:
        #     ctx.rounding = ROUND_HALF_UP
        #     dval = Decimal(value_float)
        #     rval = dval.to_integral_value()
        # s = f'{rval}'
        # or just use f-string, which rounds appropriately
        s = f'{value_float:0.0f}'
        nd = 0
    return s, nd

def get_ndec(value_str):
    s_spl = value_str.split('.')
    if len(s_spl) < 2:
        ndec = 0
    else:
        ndec = len(s_spl[1])
    return ndec

def match_ndec(value_float, str_match):
    s_spl = str_match.split('.')
    if len(s_spl) < 2:
        ndec = 0
    else:
        ndec = len(s_spl[1])
    s = f'{value_float:0.{ndec}f}'
    return s, ndec

def check_all_zero(value_str):
    # this is to determine if leading negative should be removed
    v_ = value_str.replace('-', '').replace('+', '').replace('.', '')
    all_zero = v_.count('0') == len(v_)
    return all_zero
