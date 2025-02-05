#!/usr/bin/bash

# arguments: 3 (optional) -- WC (e.g. "cW" for testing, dim6, all); "_1D" (default) or "_All" (freeze vs. profile); NDIM or not, e.g. "" (default), "_NDIM"
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/tau/'
echo "LOGDIR=${LOGDIR}"

# S="_1D"
# VF="_NDIM"
# V="-v _NDIM"

# WCs=("cW" "cHq3" "cHq1" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3" "cHB" "cll1" "cHbox" "cHDD")
# WCs=("cW" "cHq3" "cHq1" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3")

# echo "WCs=${WCs}"

echo Running combine for SM...
echo Asimov...
echo "python 1D_scan/SM_run_combine_1D.py -c 1Lepton_1T -t c -a y -e 1 -p 0.05 -l -2 -u 8 -U y > ${LOGDIR}SM_1L_1T_Asi.txt 2>&1 &"
python 1D_scan/SM_run_combine_1D.py -c 1Lepton_1T -t c -a y -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_1L_1T_Asi.txt 2>&1 &
echo "python 1D_scan/SM_run_combine_1D.py -c 2Lepton_1T -t c -a y -e 1 -p 0.05 -l -2 -u 8 -U y > ${LOGDIR}SM_2L_1T_Asi.txt 2>&1 &"
python 1D_scan/SM_run_combine_1D.py -c 2Lepton_1T -t c -a y -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_2L_1T_Asi.txt 2>&1 &
echo "python 1D_scan/LOO_SM_run_combine_1D.py -c not_tau -a y -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_tau_comb_Asi.txt 2>&1 &"
python 1D_scan/LOO_SM_run_combine_1D.py -c not_tau -a y -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_tau_comb_Asi.txt 2>&1 &
sleep 2
echo Data...
echo "python 1D_scan/SM_run_combine_1D.py -c 1Lepton_1T -t c -a n -e 1 -p 0.05 -l -2 -u 8 -U y > ${LOGDIR}SM_1L_1T_Data.txt 2>&1 &"
python 1D_scan/SM_run_combine_1D.py -c 1Lepton_1T -t c -a n -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_1L_1T_Data.txt 2>&1 &
echo "python 1D_scan/SM_run_combine_1D.py -c 2Lepton_1T -t c -a n -e 1 -p 0.05 -l -2 -u 8 -U y > ${LOGDIR}SM_2L_1T_Data.txt 2>&1 &"
python 1D_scan/SM_run_combine_1D.py -c 2Lepton_1T -t c -a n -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_2L_1T_Data.txt 2>&1 &
echo "python 1D_scan/LOO_SM_run_combine_1D.py -c not_tau -a n -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_tau_comb_Data.txt 2>&1 &"
python 1D_scan/LOO_SM_run_combine_1D.py -c not_tau -a n -e 1 -p 0.05 -l -10 -u 20 -U y > ${LOGDIR}SM_tau_comb_Data.txt 2>&1 &
