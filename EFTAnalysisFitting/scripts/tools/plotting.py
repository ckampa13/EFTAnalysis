import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator
from datetime import datetime

# nicer plot formatting
def config_plots():
    #must run twice for some reason (glitch in Jupyter)
    for i in range(2):
        plt.rcParams['figure.figsize'] = [10, 8] # larger figures
        plt.rcParams['axes.grid'] = True         # turn grid lines on
        plt.rcParams['axes.axisbelow'] = True    # put grid below points
        plt.rcParams['grid.linestyle'] = '--'    # dashed grid
        plt.rcParams.update({'font.size': 18.0})   # increase plot font size
        #plt.rcParams.update({"text.usetex": True})
        #plt.rcParams.update({"text.usetex": False})
        # to pretty print WC need these lines
        plt.rc("text", usetex=True)
        #plt.rc("text.latex", preamble=r"\usepackage{amsmath}\usepackage{amssymb}")
        plt.rc("text.latex", preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{color}")

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
def CMSify_title(ax, lumi='138', lumi_unit='fb', energy='13 TeV', prelim=True):
    lefttitle=r'$\bf{CMS}$'
    if prelim:
        lefttitle += r' $\it{Preliminary}$'
    righttitle = rf'{lumi} {lumi_unit}$^{{-1}}$ ({energy})'
    # ax.set_title(lefttitle, fontweight ='bold', loc='left')
    ax.set_title(lefttitle, loc='left')
    ax.set_title(righttitle, loc='right')
