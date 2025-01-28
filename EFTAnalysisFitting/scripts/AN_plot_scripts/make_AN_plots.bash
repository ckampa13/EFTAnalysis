#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# summary tables
# WCs (fully combined)
#echo "Making tex tables for WC limit summary..."
# python WC_summary_table.py
# dim6 only
#python WC_summary_table.py -d dim6
# dim8 only
#python WC_summary_table.py -d dim8
# tau impact
# echo "Making tex tables for impact of taus..."
# python tau_impact_table.py
# dim6 only
# python tau_impact_table.py -d dim6
# dim8 only
# python tau_impact_table.py -d dim8
# profile vs. freeze (dim6)
# echo "Making tex table comparing profile to freeze limits (dim6)..."
# python WC_prof_vs_freeze_table.py
# quad+linear vs. linear only
echo "Making tex table comparing quad+linear to linear only (dim6, dim8)..."
python WC_quad_vs_linear_table.py

# copy impact plots from plots/
# echo "Copy impact plots..."
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cW_1D.vCONFIG_VERSIONS.syst.pdf
# bash copy_impact_plots_to_AN.bash Impacts_Asimov.all_combined.cHl3_1D.vCONFIG_VERSIONS.syst.pdf

# # NLL full combination multi-panel figure
#echo "NLL vs. WC main plots (1D)..."
# echo "freeze other WCs"
# python NLL_limits_plot_from_dir.py -t f
# dim6 only
# python NLL_limits_plot_from_dir.py -t f -w dim6
# dim8 only
#python NLL_limits_plot_from_dir.py -t f -w dim8
# 1 dim6
#python NLL_limits_plot_from_dir.py -t f -w cW
#python NLL_limits_plot_from_dir.py -t f -w cll1
#python NLL_limits_plot_from_dir.py -t f -w cHbox
#python NLL_limits_plot_from_dir.py -t f -w cHDD
# debug dim8
#python NLL_limits_plot_from_dir.py -t f -w FT0
#python NLL_limits_plot_from_dir.py -t bsc -w FT0
#python NLL_limits_plot_from_dir.py -t bc -w FT0
# python NLL_limits_plot_from_dir.py -t c -w FT0
# channel
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -x 0.5 -l y
#python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w FT0 -s _1D
# profiled limits
# echo "LinearOnly fits"
# python NLL_limits_plot_from_dir.py -t f -l y -L y
##python NLL_limits_plot_from_dir.py -t f -w dim6 -l y -L y
# python NLL_limits_plot_from_dir.py -t f -w dim8 -l y -L y
# single WC
# python NLL_limits_plot_from_dir.py -t f -w cW -l y -L y
# python NLL_limits_plot_from_dir.py -t f -w cHl3 -l y -L y
# python NLL_limits_plot_from_dir.py -t f -w cll1 -l y -L y
# python NLL_limits_plot_from_dir.py -t f -w FT0 -l y -L y
#echo "profile other WCs"
###
# echo "Subchannels..."
# echo "cW"
# python NLL_limits_plot_from_dir.py -c 2Lepton_OS -t s -w cW -s _All -v _NDIM -x 0.5 -l y
# freeze
# python NLL_limits_plot_from_dir.py -c 2Lepton_OS -t s -w cW -s _1D -v _NDIM -x 0.5 -l y
###

# echo "Channels..."
# echo "cW"
####python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _All -v _NDIM -x 0.5 -l y
###python NLL_limits_plot_from_dir.py -c 2Lepton_SS -t c -w cW -s _All -v _NDIM -x 4.0 -l y
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

## tau debug
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cHq3 -s _1D -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cHq3 -s _1D -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cHl3 -s _1D -x 4 -l y
# python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cHl3 -s _1D -x 4 -l y

# echo "Full analysis..."
### top 6
# echo "cW"
# python NLL_limits_plot_from_dir.py -t f -w cW -s _All -v _NDIM -x 0.5 -l y
# python NLL_limits_plot_from_dir.py -t f -w cW -s _1D -v _NDIM -x 0.5 -l y
# echo "cHq3"
# python NLL_limits_plot_from_dir.py -t f -w cHq3 -s _All -v _NDIM -x 1.0 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHq3 -s _1D -v _NDIM -x 1.0 -l y
# echo "cHq1"
# python NLL_limits_plot_from_dir.py -t f -w cHq1 -s _All -v _NDIM -x 1.0 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHq1 -s _1D -v _NDIM -x 1.0 -l y
# echo "cHu"
# python NLL_limits_plot_from_dir.py -t f -w cHu -s _All -v _NDIM -x 2.0 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHu -s _1D -v _NDIM -x 2.0 -l y
# echo "cHd"
# python NLL_limits_plot_from_dir.py -t f -w cHd -s _All -v _NDIM -x 2.0 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHd -s _1D -v _NDIM -x 2.0 -l y
# echo "cHW"
# python NLL_limits_plot_from_dir.py -t f -w cHd -s _All -v _NDIM -x 6.0 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHd -s _1D -v _NDIM -x 6.0 -l y
# an interesting one
# echo "cHl3"
# python NLL_limits_plot_from_dir.py -t f -w cHl3 -s _All -v _NDIM -x 40 -l y
# python NLL_limits_plot_from_dir.py -t f -w cHl3 -s _1D -v _NDIM -x 40 -l y

#echo "profile vs. freeze on same plot"
#echo "Full analysis..."
### top 6
# echo "cW"
# python NLL_limits_profile_vs_freeze.py -t f -w cW -v _NDIM -x 0.2 -l y
# echo "cHq3"
# python NLL_limits_profile_vs_freeze.py -t f -w cHq3 -v _NDIM -x 0.5 -l y
# echo "cHq1"
# python NLL_limits_profile_vs_freeze.py -t f -w cHq1 -v _NDIM -x 0.5 -l y
# echo "cHu"
# python NLL_limits_profile_vs_freeze.py -t f -w cHu -v _NDIM -x 1.2 -l y
# echo "cHd"
# python NLL_limits_profile_vs_freeze.py -t f -w cHd -v _NDIM -x 1.2 -l y
# echo "cHW"
# python NLL_limits_profile_vs_freeze.py -t f -w cHW -v _NDIM -x 3.0 -l y
### next few
# echo "cHWB"
# python NLL_limits_profile_vs_freeze.py -t f -w cHWB -v _NDIM -x 10.0 -l y
# an interesting one
# echo "cHl3"
# python NLL_limits_profile_vs_freeze.py -t f -w cHl3 -v _NDIM -x 22.0 -l y
#
# echo "cHB"
# python NLL_limits_profile_vs_freeze.py -t f -w cHB -v _NDIM -x 22.0 -l y

# sample comparison
# python NLL_limits_plot_from_dir.py -t f -w cW -v _NDIM -x 0.2  -l y -fs _sample_comp
# python NLL_limits_plot_from_dir.py -t f -w cW -x 0.2  -l y -fs _sample_comp

# python NLL_limits_plot_from_dir.py -t f -w cHl3 -l y -fs _sample_comp
# all
#python NLL_limits_plot_from_dir.py -t f -w all -l y -fs _sample_comp


#####
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
# dim6 only
# python summary_NLL_limits_plot.py -w dim6
# dim8 only
# python summary_NLL_limits_plot.py -w dim8
# debug 1 WC
#python summary_NLL_limits_plot.py -w cW
#python summary_NLL_limits_plot.py -w cHq3
#python summary_NLL_limits_plot.py -w sm
# debug dim8
#python summary_NLL_limits_plot.py -w FT0
# python summary_NLL_limits_plot.py -w FT7

# signal injection -- cW
# echo "Signal injection (make NLL with full analysis and channels...)"
# python summary_NLL_limits_plot.py -i y -w cW -v 1.0

# LOO (all?)
# echo "LOO plots (make NLL with full analysis and channels...)"
# python LOO_summary_NLL_limits_plot.py -w dim6
# python LOO_summary_NLL_limits_plot.py -w dim8
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
# echo "dim8..."
# echo "all WC..."
# python WC_summary_plot.py -w all -d dim8
# echo "top 6 WC..."
# python WC_summary_plot.py -w top_6 -d dim8

# echo "WC limit summary plots v2 (horizontal band plots)..."
# echo "dim6..."
# echo "all WC..."
# python WC_summary_plot_v2.py -w all -d dim6
# echo "dim8..."
# echo "all WC..."
# python WC_summary_plot_v2.py -w all -d dim8
