#!/usr/bin/bash

# arguments: 1 (optional): which level -- "c" or "f" (default); 2 (optional) -- which channel, e.g. "all" (default); 3 (optional) -- which dim, e.g. "dim8" (default)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../output/logs/'
echo "LOGDIR=${LOGDIR}"

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

for i in $(seq 0 12);
do
    echo Running combine for clip index $i, sent to background...
    python 1D_scan/run_combine_1D.py -c $CH -w $DIM -t $L -s _1D -a y -p 0.05 -pc 0.5 -v _clip_mVVV_$i > ${LOGDIR}${CH}_${DIM}_${L}_clip_mVVV_${i}.txt 2>&1 &
done
