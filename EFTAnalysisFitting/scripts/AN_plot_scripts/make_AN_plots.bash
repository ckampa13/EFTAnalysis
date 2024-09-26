#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# NLL full combination multi-panel figure. Needs much larger labels
python NLL_limits_plot_from_dir.py -t f


#python limit_summary_plot_from_dir.py -t f
