#!/usr/bin/bash

# arguments: 1 (optional) -- profile or freeze other WCs, e.g. "_All2D" (default), "_2D"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/2D/'
echo "LOGDIR=${LOGDIR}"

if [[ -z "$1" ]]; then
    S="_All2D"
else
    S=$1
fi

echo Performing scan type: ${S}

# echo 1. Running combine cW, cHq3...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHq3 -l1 -0.5 -u1 0.5 -l2 -1.0 -u2 1.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_1_cW_cHq3${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHq3 -l1 -0.5 -u1 0.5 -l2 -1.0 -u2 1.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_1_cW_cHq3${S}.txt 2>&1 &
# echo 2. Running combine cW, cHl3...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHl3 -l1 -0.5 -u1 0.5 -l2 -15.0 -u2 45.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_2_cW_cHl3${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHl3 -l1 -0.5 -u1 0.5 -l2 -15.0 -u2 45.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_2_cW_cHl3${S}.txt 2>&1 &
# echo 3. Running combine cW, cHW...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHW -l1 -0.5 -u1 0.5 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_3_cW_cHW${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cW -w2 cHW -l1 -0.5 -u1 0.5 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_3_cW_cHW${S}.txt 2>&1 &
# echo 4. Running combine cHq3, cHu...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHu -l1 -1.0 -u1 1.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_4_cHq3_cHu${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHu -l1 -1.0 -u1 1.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_4_cHq3_cHu${S}.txt 2>&1 &
# echo 5. Running combine cHu, cHd...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHd -l1 -3.0 -u1 3.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_5_cHu_cHd${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHd -l1 -3.0 -u1 3.0 -l2 -3.0 -u2 3.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_5_cHu_cHd${S}.txt 2>&1 &
# echo 6. Running combine cHu, cHW...
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHW -l1 -3.0 -u1 3.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_6_cHu_cHW${S}.txt 2>&1 &
# python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHu -w2 cHW -l1 -3.0 -u1 3.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_6_cHu_cHW${S}.txt 2>&1 &
echo 7. Running combine cHq3, cHq1...
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHq1 -l1 -1.0 -u1 1.0 -l2 -2.0 -u2 2.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_7_cHq3_cHq1${S}.txt 2>&1 &
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHq1 -l1 -1.0 -u1 1.0 -l2 -2.0 -u2 2.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_7_cHq3_cHq1${S}.txt 2>&1 &
echo 8. Running combine cHq3, cHW...
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHW -l1 -1.0 -u1 1.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_8_cHq3_cHW${S}.txt 2>&1 &
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq3 -w2 cHW -l1 -1.0 -u1 1.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_8_cHq3_cHW${S}.txt 2>&1 &
echo 9. Running combine cHq1, cHW...
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq1 -w2 cHW -l1 -2.0 -u1 2.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a y > ${LOGDIR}comb_Asimov_9_cHq1_cHW${S}.txt 2>&1 &
python 2D_scan/run_combine_2D.py -s ${S} -t f -w1 cHq1 -w2 cHW -l1 -2.0 -u1 2.0 -l2 -6.0 -u2 6.0 -p1 0.01 -p2 0.01 -v _NDIM -U y -a n > ${LOGDIR}comb_Data_9_cHq1_cHW${S}.txt 2>&1 &
