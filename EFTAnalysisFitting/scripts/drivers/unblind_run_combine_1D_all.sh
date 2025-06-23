#!/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/combine/'
# path for grabbing versions_dict
VDICT_DIR=$(realpath "${SCRIPT_DIR}/../")

echo "LOGDIR=${LOGDIR}"
# echo "VDICT_DIR=${VDICT_DIR}"

# arguments: 4 (optional)
# 1. Data or Asimov? "Asimov" (default), "Data"
# 2. WC to run combine for, e.g. "all" (default), "dim6", "dim8", "cW";
# 3. level, e.g. "f" (default), "c", "s", "b";
# 4. split WCs to different procs? "n" (default), "y"
# 5. NDIM or not, e.g. "" (default), "_NDIM"

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

if [[ -z "$2" ]]; then
    W="all"
else
    W=$2
fi

# handle the different WC input types
if [[ "$W" == "all" || "$W" == "dim6" || "$W" == "dim8" ]]; then
    Wmany=true
else
    Wmany=false
fi

if [[ -z "$3" ]]; then
    T="f"
else
    T=$3
fi

if [ "$T" = "f"  ]; then
    # T is equal to 'f', only use one channel
    TB="True"
else
    # T is not equal to 'f', loop through all channel
    TB="False"
fi

if [[ -z "$4" ]]; then
    S="n"
else
    S=$4
fi

if [ "$S" = "y" ]; then
    #SB="True"
    if [ "$Wmany" = true ]; then
        mapfile -t WCloop < <(python -c "
import sys
sys.path.append('${VDICT_DIR}')
from CONFIG_VERSIONS import WC_ALL, dim6_WCs, dim8_WCs
W_ = \"${W}\"
if W_ == \"all\":
    WCs = WC_ALL
elif W_ == \"dim6\":
    WCs = dim6_WCs
else:
    WCs = dim8_WCs
for WC in WCs:
    print WC
        ")
    else
        WCloop=(${W})
    fi
else
    #SB="False"
    WCloop=($W)
fi

if [[ -z "$5" ]]; then
    V=""
    VF=""
else
    if [[ "$5" == "" ]]; then
        V=""
        VF=""
    else
        V="-v $5"
        VF=$5
    fi
fi

echo "A=${A}, W=${W}, T=${T}, S=${S}, V=${V}"
echo

# Adjust PYTHONPATH if needed, or run from same directory
while read channel version; do
    echo "Running for channel=$channel, version=$version"
    for WC in "${WCloop[@]}"; do
        echo "WC=${WC}"
        if [ "$T" = "f"  ]; then
            CHF="full_analysis"
        else
            CHF=${channel}
        fi
        echo "python 1D_scan/run_combine_1D.py -c $channel -w ${WC} -t ${T} -s _1D -p 0.01 -pc 0.05 -U y -a ${AS} > ${LOGDIR}run_combine_1D_${A}_${CHF}_${T}_${WC}_${VF}.txt 2>&1 &"
        python 1D_scan/run_combine_1D.py -c $channel -w ${WC} -t ${T} -s _1D -p 0.01 -pc 0.05 -U y -a ${AS} > ${LOGDIR}run_combine_1D_${A}_${CHF}_${T}_${WC}_${VF}.txt 2>&1 &
    done
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
