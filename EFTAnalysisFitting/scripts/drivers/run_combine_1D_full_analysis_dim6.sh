#!/usr/bin/bash

WCs=('cW' 'cHbox' 'cHDD' 'cHl3' 'cHq1' 'cHq3' 'cHW' 'cHWB' 'cll1' 'cHB' 'cHu' 'cHd')

# arguments: 1 (optional) -- profile or freeze other WCs, e.g. "_2D" (default), "_All2D"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../output/logs/full_analysis/1D/'
echo "LOGDIR=${LOGDIR}"

for WC in "${WCs[@]}"; do
    echo $WC
    echo "python 1D_scan/run_combine_1D.py -w $WC -t f -s _1D -a y -p 0.01 -pc 0.05 > ${LOGDIR}${WC}_1D.txt 2>&1 &"
    python 1D_scan/run_combine_1D.py -w $WC -t f -s _1D -a y -p 0.01 -pc 0.05 > ${LOGDIR}${WC}_1D.txt 2>&1 &
    echo
done
