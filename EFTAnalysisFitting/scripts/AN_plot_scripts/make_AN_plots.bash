#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# copy impact plots from plots/
# echo "Copy impact plots..."
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cW_1D.vCONFIG_VERSIONS.syst.pdf
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cHl3_1D.vCONFIG_VERSIONS.syst.pdf

# # NLL full combination multi-panel figure
# echo "NLL vs. WC main plots (1D)..."
# python NLL_limits_plot_from_dir.py -t f
# 1 dim6
#python NLL_limits_plot_from_dir.py -t f -w cW
# debug dim8
#python NLL_limits_plot_from_dir.py -t f -w FT0
#python NLL_limits_plot_from_dir.py -t bsc -w FT0
#python NLL_limits_plot_from_dir.py -t bc -w FT0
python NLL_limits_plot_from_dir.py -t c -w FT0

# # yield summary plot with bin limits in bottom panel
# # make tables
# # FIXME! Move this to this repo?
# echo "Make Tables..."
# python /home/ckampa/coding/VVVTable/EFT_yields/make_tables_from_combine.py
# # make plot
# echo "Make yield summary plot..."
# python yield_summary_plots.py -w cW

# # NLL full combination and channels
# # no signal injection -- WCs and SM
# echo "Make NLL with full analysis and channels..."
# python summary_NLL_limits_plot.py
# debug 1 WC
#python summary_NLL_limits_plot.py -w cW
#python summary_NLL_limits_plot.py -w cHq3
# python summary_NLL_limits_plot.py -w sm
# degug dim8
python summary_NLL_limits_plot.py -w FT0

# signal injection -- cW
# echo "Signal injection (make NLL with full analysis and channels...)"
# python summary_NLL_limits_plot.py -i y -w cW -v 1.0

# LOO (all?)
# echo "LOO plots (make NLL with full analysis and channels...)"
# python LOO_summary_NLL_limits_plot.py -w dim6
# debug, cW only
#python LOO_summary_NLL_limits_plot.py -w cW

# echo "WC limit summary plots (horizontal band plots)..."
# echo "dim6..."
# echo "all WC..."
# python WC_summary_plot.py -w all -d dim6
# echo "top 6 WC..."
# python WC_summary_plot.py -w top_6 -d dim6
# echo "dim8..."
# echo "all WC..."
# python WC_summary_plot.py -w all -d dim8
# echo "top 6 WC..."
# python WC_summary_plot.py -w top_6 -d dim8
