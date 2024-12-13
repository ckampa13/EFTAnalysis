#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# summary tables
# WCs (fully combined)
#echo "Making tex tables for WC limit summary..."
#python WC_summary_table.py
# tau impact
#echo "Making tex tables for impact of taus..."
#python tau_impact_table.py

# copy impact plots from plots/
# echo "Copy impact plots..."
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cW_1D.vCONFIG_VERSIONS.syst.pdf
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cHl3_1D.vCONFIG_VERSIONS.syst.pdf

# # NLL full combination multi-panel figure
echo "NLL vs. WC main plots (1D)..."
#echo "freeze other WCs"
#python NLL_limits_plot_from_dir.py -t f
# 1 dim6
#python NLL_limits_plot_from_dir.py -t f -w cW
# debug dim8
#python NLL_limits_plot_from_dir.py -t f -w FT0
#python NLL_limits_plot_from_dir.py -t bsc -w FT0
#python NLL_limits_plot_from_dir.py -t bc -w FT0
#python NLL_limits_plot_from_dir.py -t c -w FT0
# profiled limits
echo "profile other WCs"
# echo "Channels..."
# echo "cW"
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton -t c -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _All -v _NDIM -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _All -v _NDIM -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_OS -t c -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_OS_2FJ -t c -w cW -s _All -v _NDIM -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 0Lepton_2FJ -t c -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -t c -w cW -s _All -v _NDIM -x 0.5 -l y
# fast scans
# python NLL_limits_plot_from_dir.py -c 0Lepton_2FJ -t c -w cW -s _All -f y -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -t c -w cW -s _All -f y -v _NDIM -x 0.5 -l y
#### python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _All -v _NDIM -x 2 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_OS -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 0Lepton_2FJ -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -t c -w cW -s _1D -v _NDIM -x 0.5 -l y
# using 1D sample
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _1D -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton -t c -w cW -s _1D -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 2Lepton_OS -t c -w cW -s _1D -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 0Lepton_2FJ -t c -w cW -s _1D -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -t c -w cW -s _1D -x 0.5 -l y

# echo "cHl3"
#python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cHl3 -s _All -v _NDIM -x 40 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cHl3 -s _All -v _NDIM -x 60 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cHl3 -s _All -v _NDIM -x 100 -l y
#python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cHl3 -s _1D -v _NDIM -x 40 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cHl3 -s _1D -v _NDIM -x 60 -l y

echo "Full analysis..."
echo "cW"
python NLL_limits_plot_from_dir.py -t f -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -t f -w cW -s _1D -v _NDIM -x 0.5 -l y

# recreate the main freeze plot (adding limit to legend)
# note this comparison doesn't make sense until we have all channels combined in the profile fit!
# python NLL_limits_plot_from_dir.py -t f -w cW -s _1D -x 0.5 -l y

# # yield summary plot with bin limits in bottom panel
# # make tables
# # FIXME! Move this to this repo?
# echo "Make Tables..."
#python /home/ckampa/coding/VVVTable/EFT_yields/make_tables_from_combine.py
# # make plot
# echo "Make yield summary plot..."
# python yield_summary_plots.py -w cW

# # NLL full combination and channels
# # no signal injection -- WCs and SM
# echo "Make NLL with full analysis and channels..."
# python summary_NLL_limits_plot.py
# dim8 only
#python summary_NLL_limits_plot.py -w dim8
# debug 1 WC
#python summary_NLL_limits_plot.py -w cW
#python summary_NLL_limits_plot.py -w cHq3
#python summary_NLL_limits_plot.py -w sm
# degug dim8
#python summary_NLL_limits_plot.py -w FT0
# python summary_NLL_limits_plot.py -w FT7

# signal injection -- cW
# echo "Signal injection (make NLL with full analysis and channels...)"
# python summary_NLL_limits_plot.py -i y -w cW -v 1.0

# LOO (all?)
# echo "LOO plots (make NLL with full analysis and channels...)"
# python LOO_summary_NLL_limits_plot.py -w dim6
# debug, cW only
#python LOO_summary_NLL_limits_plot.py -w cW
# LOO (all_tau)
#python all_tau_LOO_summary_NLL_limits_plot.py -w cW

#echo "WC limit summary plots (horizontal band plots)..."
# echo "dim6..."
# echo "all WC..."
# python WC_summary_plot.py -w all -d dim6
# echo "top 6 WC..."
# python WC_summary_plot.py -w top_6 -d dim6
#echo "dim8..."
#echo "all WC..."
#python WC_summary_plot.py -w all -d dim8
#echo "top 6 WC..."
#python WC_summary_plot.py -w top_6 -d dim8

# echo "WC limit summary plots v2 (horizontal band plots)..."
# echo "dim6..."
# echo "all WC..."
# python WC_summary_plot_v2.py -w all -d dim6
# echo "dim8..."
# echo "all WC..."
# python WC_summary_plot_v2.py -w all -d dim8
