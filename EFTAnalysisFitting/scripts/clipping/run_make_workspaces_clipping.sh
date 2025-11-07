#!/usr/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/workspaces/clipping/'

echo "LOGDIR=${LOGDIR}"
# arguments: 1 (optional): which level -- "c" or "f" (default); 2 (optional) -- which channel, e.g. "all" (default); 3 (optional) -- which dim, e.g. "dim8" (default)

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

echo "L=${L}, CH=${CH}, DIM=${DIM}"
echo

if [ "$L" = "f"  ]; then
    CHF="full_analysis"
else
    CHF=${CH}
fi

#for i in $(seq 0 12);
#for i in $(seq 0 14); # adding a few points just below 1 TeV
# full
for i in $(seq 0 17); # adding a few points just below 1 TeV
# first half
# for i in $(seq 0 8); # adding a few points just below 1 TeV
# second half
# for i in $(seq 9 17); # adding a few points just below 1 TeV
do
    echo Making workspaces for clip index $i...
    echo "python3 tools/make_workspaces.py -c $CH -d $DIM -t $L -v _clip_mVVV_$i -U y > ${LOGDIR}make_workspaces_${CHF}_${L}_${DIM}_clip_${i}.txt 2>&1 &"
    python3 tools/make_workspaces.py -c $CH -d $DIM -t $L -v _clip_mVVV_$i -U y > ${LOGDIR}make_workspaces_${CHF}_${L}_${DIM}_clip_${i}.txt 2>&1 &
done
