#!/bin/bash

### ACTIVATE CONDA ENVIRONMENT ###
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

### FIGURES ###
# Fig 11 (yield summary)
# make summary dataframe based on fit with toys (ROOT input, pkl output)
# -w "WC"
#python Fig11_process_yields_limits.py -w cW
# make the plot (pkl input)
# -w "WC"
#python Fig11_unblind_yield_summary_plots.py -w cW

# Fig 12 (2D plots)
# test 1 WC pair
# python Fig12_2D_contour_plots.py -w1 cW -w2 cHq3 -f y
# python Fig12_2D_contour_plots.py -w1 cW -w2 cHq3 -f n
# run all
python Fig12_2D_contour_plots.py -w1 all_paper -w2 all_paper -f y
python Fig12_2D_contour_plots.py -w1 all_paper -w2 all_paper -f n


# Fig 13 (clipping)

# Fig 14 (template fit)
# python Fig14_template_fit.py

# Fig 15 (SM sensitivity)
# -w "WC" -U "unblind directory" -a "Asimov" -OD "OverlayData"
#python Fig15_summary_NLL_limits_plot.py -w sm -U y -a y -OD y

### TABLES ###
