#!/usr/bin/bash

# arguments: 1 (optional): which level -- "c" or "f" (default); 2 (optional) -- which channel, e.g. "all" (default); 3 (optional) -- which dim, e.g. "dim8" (default)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../output/logs/'
echo "LOGDIR=${LOGDIR}"

WCs_dim6=("cW" "cHbox" "cHDD" "cHl3" "cHq1" "cHq3" "cHW" "cHWB" "cll1" "cHB" "cHu" "cHd")
WCs_dim8=("FS0" "FS1" "FS2" "FM0" "FM1" "FM2" "FM3" "FM4" "FM5" "FM7" "FT0" "FT1" "FT2" "FT3" "FT4" "FT5" "FT6" "FT7" "FT8" "FT9")

if [[ -z "$1" ]]; then
    L="f"
else
    L=$1
fi

if [[ -z "$2" ]]; then
    CH="all"
else
    CH=$2
fi

if [[ -z "$3" ]]; then
    DIM="dim8"
else
    DIM=$3
fi

# pick appropriate WC
if [[ "$DIM" == "dim6" ]]; then
    selected_list=("${WCs_dim6[@]}")
    P="0.005"
elif [[ "$DIM" == "dim8" ]]; then
    selected_list=("${WCs_dim8[@]}")
    P="0.05"
else
    echo "Error: DIM must be either 'dim6' or 'dim8'."
        exit 1
fi

for WC in "${selected_list[@]}";
do
    echo Running combine for WC $WC, sent to background...
    python 1D_scan/run_combine_1D.py -c $CH -w $WC -t $L -s _1D -a y -p ${P} -pc 0.5 > ${LOGDIR}main_ana_${CH}_${DIM}_${WC}_${L}.txt 2>&1 &
done
