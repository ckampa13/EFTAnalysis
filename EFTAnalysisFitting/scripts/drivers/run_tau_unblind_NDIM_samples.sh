#!/usr/bin/bash

echo Running scripts for NDIM file for tau channels...
echo Combining cards channel level...
python tools/combine_cards.py -v _NDIM -U y
echo Combining cards all taus...
python tools/LOO_combine_cards.py -c not_tau -v _NDIM -U y
echo Making workspaces for channel level...
python tools/make_workspaces.py -c 1Lepton_1T -d dim6 -t c -v _NDIM -U y
python tools/make_workspaces.py -c 2Lepton_1T -d dim6 -t c -v _NDIM -U y
echo Making workspaces for tau combination...
python tools/LOO_make_workspaces.py -c not_tau -d dim6 -v _NDIM -U y
echo Running combine...
echo Asimov...
# cW only tests -- update -w to "dim6". also consider adding -s _All for profiling in another run
python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w cW -t c -s _1D -a y -p 0.05 -pc 0.5 -v _NDIM -U y
python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w cW -t c -s _1D -a y -p 0.05 -pc 0.5 -v _NDIM -U y
python 1D_scan/LOO_run_combine_1D.py -c not_tau -w cW -s _1D -a y -p 0.05 -pc 0.5 -v _NDIM -U y
echo Data...
python 1D_scan/run_combine_1D.py -c 1Lepton_1T -w cW -t c -s _1D -a n -p 0.05 -pc 0.5 -v _NDIM -U y
python 1D_scan/run_combine_1D.py -c 2Lepton_1T -w cW -t c -s _1D -a n -p 0.05 -pc 0.5 -v _NDIM -U y
python 1D_scan/LOO_run_combine_1D.py -c not_tau -w cW -s _1D -a n -p 0.05 -pc 0.5 -v _NDIM -U y

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
