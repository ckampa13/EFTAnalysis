#!/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/workspaces/'
# path for grabbing versions_dict
VDICT_DIR=$(realpath "${SCRIPT_DIR}/../")

echo "LOGDIR=${LOGDIR}"
# echo "VDICT_DIR=${VDICT_DIR}"

# arguments: 3 (optional)
# 1. dim to make workspaces for, e.g. "all" (default), "dim6", "dim8";
# 2. level, e.g. "f" (default), "c", "s", "b";
# 3. NDIM or not, e.g. "" (default), "_NDIM"
# for "b" and "f" I recommend running dim6 and dim8 independently

if [[ -z "$1" ]]; then
    D="all"
else
    D=$1
fi

if [[ -z "$2" ]]; then
    T="f"
else
    T=$2
fi

if [ "$T" = "f"  ]; then
    #echo "T is equal to 'f'"
    TB="True"
else
    # echo "T is not equal to 'f'"
    TB="False"
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

echo "D=${D}, T=${T}, V=${V}"
echo


# Adjust PYTHONPATH if needed, or run from same directory
while read channel version; do
    if [ "$T" = "f"  ]; then
        CHF="full_analysis"
    else
        CHF=${channel}
    fi
    echo "Running for channel=$channel, version=$version"
    echo "python tools/make_workspaces.py -c $channel -d ${D} -t ${T} -U y ${V} > ${LOGDIR}make_workspaces_${CHF}_${T}_${D}${VF}.txt 2>&1 &"
    python tools/make_workspaces.py -c $channel -d ${D} -t ${T} -U y ${V} > ${LOGDIR}make_workspaces_${CHF}_${T}_${D}${VF}.txt 2>&1 &
done < <(python -c "
import sys
sys.path.append('${VDICT_DIR}')
from CONFIG_VERSIONS import versions_dict
# for ch, meta in versions_dict.items():
for i, tup in enumerate(sorted(versions_dict.items())):
    ch, meta = tup
    if ${TB}: # if full analysis, only use one channel
        if i > 0:
            continue
    print '%s %s' % (ch, meta[\"v\"])
")
