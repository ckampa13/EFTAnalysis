#!/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/grid/clipping/'

DATE="07-13-25"

echo "LOGDIR=${LOGDIR}"
echo "DATE=${DATE}"

clip_inds=({0..17})

# arguments: 1 (optional)
# 1. Data or Asimov? "Asimov" (default), "Data"

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

echo "A=${A}"

for i in "${clip_inds[@]}"; # adding a few points just below 1 TeV
do
    echo "clip_ind=${i}"
    suff="_clip_mVVV_${i}"
    echo "python3 tools/hadd_grid_jobs.py -d clipping/${DATE}/ -w all -s _1D -a ${AS} -U y -v ${suff} > ${LOGDIR}hadd_grid_jobs_asi_${AS}${suff}.txt 2>&1 &"
    python3 tools/hadd_grid_jobs.py -d clipping/${DATE}/ -w all -s _1D -a ${AS} -U y -v ${suff} > ${LOGDIR}hadd_grid_jobs_asi_${AS}${suff}.txt 2>&1 &
done

