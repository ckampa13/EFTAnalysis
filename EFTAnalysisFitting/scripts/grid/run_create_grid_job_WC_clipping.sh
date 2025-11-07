#!/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/grid/clipping/'

echo "LOGDIR=${LOGDIR}"

WCs_dim6=("cW" "cHbox" "cHDD" "cHl3" "cHq1" "cHq3" "cHW" "cHWB" "cll1" "cHB" "cHu" "cHd")
WCs_dim8=("FS0" "FS1" "FS2" "FM0" "FM1" "FM2" "FM3" "FM4" "FM5" "FM7" "FT0" "FT1" "FT2" "FT3" "FT4" "FT5" "FT6" "FT7" "FT8" "FT9")
WCs=("${WCs_dim6[@]}" "${WCs_dim8[@]}")
# WCs=("FM7") # fix in MISC_CONFIGS

# YN=("y" "n")

# arguments: 2 (optional)
# 1. Data or Asimov? "Asimov" (default), "Data"
# 2. Syst or Stat? "Syst" (default), "Stat"

# clip_inds=$(seq 0 17)

# args
if [[ -z "$1" ]]; then
    A="Asimov"
else
    A=$1
fi

if [[ "$A" == "Asimov" ]]; then
    AS="y"
else
    AS="n"
fi

if [[ -z "$2" ]]; then
    S="Syst"
else
    S=$2
fi

if [[ "$S" == "Syst" ]]; then
    SS="y"
else
    SS="n"
fi

echo "A=${A}, S=${S}"

for WC in "${WCs[@]}"; do
    echo "WC=$WC"
    if [[ "${WCs_dim6[@]}" =~ "$WC" ]]; then
        # SP=200 # 07-13-25 -- some jobs took too long
        SP=100 # 11-06-25
    else
        # SP=90 # 07-13-25 -- some jobs took too long
        SP=50 # 11-06-25
    fi
    # for asi in "${YN[@]}"; do
    #     echo "asi=$asi"
    #     for syst in "${YN[@]}"; do
    #         echo "syst=$syst"
    echo "python3 grid/create_grid_job_WC_clipping.py -c all -w $WC -a ${AS} -S ${SS} -PRP 4 -SP $SP > ${LOGDIR}create_grid_job_full_analysis_f_${WC}_asi_${AS}_syst_${SS}_clip_all.txt 2>&1 &"
    python3 grid/create_grid_job_WC_clipping.py -c all -w $WC -a ${AS} -S ${SS} -PRP 4 -SP $SP > ${LOGDIR}create_grid_job_full_analysis_f_${WC}_asi_${AS}_syst_${SS}_clip_all.txt 2>&1 &
        # done
    # done
done

