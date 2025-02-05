#!/usr/bin/bash

# arguments: 3 (optional) -- WC (e.g. "cW" for testing, dim6, all); "_1D" (default) or "_All" (freeze vs. profile); NDIM or not, e.g. "" (default), "_NDIM"
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/tau/'
echo "LOGDIR=${LOGDIR}"

# if [[ -z "$1" ]]; then
#     WC="cW"
# else
#     WC=$1
# fi

# if [[ -z "$2" ]]; then
#     S="_1D"
# else
#     S=$2
# fi

# if [[ -z "$3" ]]; then
#     V=""
#     VF=""
# else
#     if [[ "$3" == "" ]]; then
#         V=""
#         VF=""
#     else
#         V="-v $3"
#         VF=$3
#     fi
# fi

# echo "WC=${WC}, V=${V}"
# echo

S="_All"
VF="_NDIM"
V="-v _NDIM"

# WCs=("cW" "cHq3" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3" "cHB" "cll1" "cHbox" "cHDD")
# WCs=("cW" "cHq3" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3")
#WCs=("cW" "cHq3" "cHq1")
WCs=("cW" "cHq1" "cHu" "cHd")

echo "WCs=${WCs}"
echo

echo Running combine...
for WC in "${WCs[@]}"; do
    echo $WC
    echo Asimov...
    # cW only tests -- update -w to "dim6". also consider adding -s _All for profiling in another run
    # echo "python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &"
    # python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &
    # echo "python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &"
    # python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &
    echo "python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Asi_${WC}${S}${VF}.txt 2>&1 &"
    python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Asi_${WC}${S}${VF}.txt 2>&1 &
    sleep 2
    echo Data...
    # echo "python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Data_${WC}${S}${VF}.txt 2>&1 &"
    # python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Data_${WC}${S}${VF}.txt 2>&1 &
    # echo "python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Data_${WC}${S}${VF}.txt 2>&1 &"
    # python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Data_${WC}${S}${VF}.txt 2>&1 &
    echo "python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Data_${WC}${S}${VF}.txt 2>&1 &"
    python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Data_${WC}${S}${VF}.txt 2>&1 &
done
