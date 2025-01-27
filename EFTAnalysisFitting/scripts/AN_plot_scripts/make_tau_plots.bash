#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate HCOMB

# files for unblinding
UNBLIND=true
#UNBLIND=false

# use asimov or data
# ASIMOV=true
ASIMOV=false

if $UNBLIND; then
  UNBL_STR="y"
else
  UNBL_STR="n"
fi

# if $ASIMOV; then
#   ASI_STR="y"
# else
#   ASI_STR="n"
# fi

echo "Generating plots for tau channels..."
echo "Input files for unblinding? $UNBL_STR"
# echo "Asimov dataset? $ASI_STR"
echo

ASI_STRS=("n" "y")

for ASI_STR in "${ASI_STRS[@]}"
do
  echo "Asimov dataset? $ASI_STR"
  # NLL vs. WC
  echo "NLL vs. WC main plots..."
  # 1D file
  #echo "1D Samples:"
  ## cW only -- tests
  # python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -l y -U $UNBL_STR -a $ASI_STR # 1L
  # python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -l y -U $UNBL_STR -a $ASI_STR # 2L
  # python NLL_limits_plot_from_dir.py -c tau -t f -w cW -s _1D -l y -U $UNBL_STR -a $ASI_STR # combined
  echo "NDIM Samples:"
  # cW only -- tests
  python NLL_limits_plot_from_dir.py -c 1Lepton_1T -t c -w cW -s _1D -l y -v _NDIM -U $UNBL_STR -a $ASI_STR # 1L
  python NLL_limits_plot_from_dir.py -c 2Lepton_1T -t c -w cW -s _1D -l y -v _NDIM  -U $UNBL_STR -a $ASI_STR # 2L
  python NLL_limits_plot_from_dir.py -c tau -t f -w cW -s _1D -l y -v _NDIM -U $UNBL_STR -a $ASI_STR # combined
done

## OLD BELOW -- to consider adding
# dim6, then dim8 -- MAIN
#python NLL_limits_plot_from_dir.py -c tau -t f -w dim6 -s _1D -l y -U y -a n
#python NLL_limits_plot_from_dir.py -c tau -t f -w dim8 -s _1D -l y -U y -a n

# NDIM file
#echo "NDIM Samples:"
# cW only -- tests
#python NLL_limits_plot_from_dir.py -c tau -t f -w cW -s _1D -l y -v _NDIM -U y -a n
# dim6, then dim8 -- MAIN
#python NLL_limits_plot_from_dir.py -c tau -t f -w dim6 -s _1D -l y -v _NDIM -U y -a n
#python NLL_limits_plot_from_dir.py -c tau -t f -w dim8 -s _1D -l y -v _NDIM -U y -a n


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
