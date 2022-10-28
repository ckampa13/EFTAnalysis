#!/bin/bash
# Run plotting scripts for all levels of the analysis, based on channel info in datacard_dict.

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# run NLL plots
python NLL_limits_plot_from_dir.py
# run limit summary plots
python limit_summary_plot_from_dir.py
