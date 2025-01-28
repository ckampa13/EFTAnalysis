#!/usr/bin/bash

# arguments: 3 (optional) -- WC (e.g. "cW" for testing, dim6, all); "_1D" (default) or "_All" (freeze vs. profile); NDIM or not, e.g. "" (default), "_NDIM"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/tau/'
echo "LOGDIR=${LOGDIR}"

if [[ -z "$1" ]]; then
    WC="cW"
else
    WC=$1
fi

if [[ -z "$2" ]]; then
    S="_1D"
else
    S=$2
fi

if [[ -z "$3" ]]; then
    V=""
    VF=""
else
    if [[ "$3" == "" ]]; then
        V=""
        VF=""
    else
        V="-v $3"
        VF=$3
    fi
fi

echo "WC=${WC}, V=${V}"
echo

echo Running combine...
echo Asimov...
# cW only tests -- update -w to "dim6". also consider adding -s _All for profiling in another run
echo "python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &
echo "python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Asi_${WC}${S}${VF}.txt 2>&1 &
echo "python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Asi_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a y -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Asi_${WC}${S}${VF}.txt 2>&1 &
echo Data...
echo "python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Data_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}1L_1T_Data_${WC}${S}${VF}.txt 2>&1 &
echo "python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Data_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w ${WC} -t c -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}2L_1T_Data_${WC}${S}${VF}.txt 2>&1 &
echo "python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Data_${WC}${S}${VF}.txt 2>&1 &"
python 1D_scan/LOO_run_combine_1D.py -c not_tau -w ${WC} -s ${S} -a n -p 0.05 -pc 0.5 -U y ${V} > ${LOGDIR}tau_comb_Data_${WC}${S}${VF}.txt 2>&1 &

# OLD BELOW
# arguments: 1 (optional) -- profile or freeze other WCs, e.g. "_All2D" (default), "_2D"
# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
# LOGDIR=$SCRIPT_DIR'/../../output/logs/2D/'
# echo "LOGDIR=${LOGDIR}"

# if [[ -z "$1" ]]; then
#     S="_All2D"
# else
#     S=$1
# fi

# echo Performing scan type: ${S}

# echo 1. Running combine cW, cHq3...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHq3 -l1 -0.5 -u1 0.5 -l2 -1.0 -u2 1.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}1_cW_cHq3${S}.txt 2>&1 &
# echo 2. Running combine cW, cHl3...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHl3 -l1 -0.5 -u1 0.5 -l2 -15.0 -u2 45.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}2_cW_cHl3${S}.txt 2>&1 &
# echo 3. Running combine cW, cHW...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHW -l1 -0.5 -u1 0.5 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}3_cW_cHW${S}.txt 2>&1 &
# echo 4. Running combine cHq3, cHu...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHu -l1 -1.0 -u1 1.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}4_cHq3_cHu${S}.txt 2>&1 &
# echo 5. Running combine cHu, cHd...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHd -l1 -3.0 -u1 3.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}5_cHu_cHd${S}.txt 2>&1 &
# echo 6. Running combine cHu, cHW...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHW -l1 -3.0 -u1 3.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM > ${LOGDIR}6_cHu_cHW${S}.txt 2>&1 &
