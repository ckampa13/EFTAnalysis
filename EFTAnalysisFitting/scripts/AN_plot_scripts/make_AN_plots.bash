#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# NLL full combination multi-panel figure. Needs much larger labels
#python NLL_limits_plot_from_dir.py -t f

# yield summary plot with bin limits in bottom panel
#python yield_summary_plots.py -w cW

# NLL full combination and channels
# no signal injection -- WCs and SM
#python summary_NLL_limits_plot.py
# debug 1 WC
python summary_NLL_limits_plot.py -w cW

# signal injection -- cW
# python summary_NLL_limits_plot.py -i y -w cW -v 1.0

#python limit_summary_plot_from_dir.py -t f
