#!/bin/bash
# CAUTION! Do NOT use "all" for WC flag -- this is no longer supported with the
# additional arguments needed to promote some NPs to POIs.

# directories
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/combine/'
# path for grabbing versions_dict
VDICT_DIR=$(realpath "${SCRIPT_DIR}/../")

# WCsNDIM=("cW" "cHq3" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3" "cHB") # original
WCsNDIM=("cW" "cHq3" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3" "cHB" "cll1" "cHbox" "cHDD") # all dim6
# WCsNDIM=("cll1" "cHbox" "cHDD") # temp to fill the missing WCs
dim6_WCs=("cW" "cHq3" "cHq1" "cHu" "cHd" "cHW" "cHWB" "cHl3" "cHB" "cll1" "cHbox" "cHDD")

echo "LOGDIR=${LOGDIR}"
# echo "VDICT_DIR=${VDICT_DIR}"

# arguments: 4 (optional)
# 1. Data or Asimov? "Asimov" (default), "Data"
# 2. WC to run combine for, e.g. "dim6" (default), "dim8", "NDIM", "cW";
# 3. level, e.g. "f" (default), "c", "s", "b";
# 4. split WCs to different procs? "n" (default), "y"
# 5. NDIM or not, e.g. "" (default), "_NDIM"

# extras
PRP="4" # pointsRandProf to use
PRPS="n" # don't use pointsRandProf for stat only calculation

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

if [[ -z "$2" ]]; then
    W="dim6"
else
    W=$2
fi

# handle the different WC input types
if [[ "$W" == "all" || "$W" == "dim6" || "$W" == "dim8" || "$W" == "NDIM" ]]; then
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
    UP="y" # UseProfileLimits (save some time)
else
    # T is not equal to 'f', loop through all channel
    TB="False"
    UP="n" # don't UseProfileLimits -- ranges are channel dependent
fi

if [[ -z "$4" ]]; then
    S="n"
else
    S=$4
fi

if [ "$S" = "y" ]; then
    #SB="True"
    if [ "$Wmany" = true ]; then
        if [ "$W" = "NDIM" ]; then
            WCloop=("${WCsNDIM[@]}")
        else
            mapfile -t WCloop < <(python3 -c "
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
    # print WC
    print(WC)
            ")
        fi
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
echo "WCloop=${WCloop[@]}"
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
        # check whether dim6 or dim8
        if [ "$Wmany" = true  ]; then
            if [[ ${WC} = "dim8" || ( ! ${dim6_WCs[@]} =~ $WC && ! ${WC} = "dim6" ) ]]; then
                PNP="y"
                PRPcurr=$PRP
            else
                # if ever promoting dim6 NPs to POIs, switch this to "y"
                PNP="n"
                PRPcurr="0"
            fi
        else
            if [[ ${dim6_WCs[@]} =~ $WC ]]; then
                # if ever promoting dim6 NPs to POIs, switch this to "y"
                PNP="n"
                PRPcurr="0"
            else
                PNP="y"
                PRPcurr=$PRP
            fi
        fi
        echo "python3 1D_scan/run_combine_1D.py -c $channel -w ${WC} -t ${T} -s _1D -p 0.01 -pc 0.05 -U y -a ${AS} -T y -J n -UP $UP -PRP $PRPcurr -PRPS $PRPS -PNP $PNP ${V} > ${LOGDIR}run_combine_1D_${A}_${CHF}_${T}_${WC}_${VF}.txt 2>&1 &"
        python3 1D_scan/run_combine_1D.py -c $channel -w ${WC} -t ${T} -s _1D -p 0.01 -pc 0.05 -U y -a ${AS} -T y -J n -UP $UP -PRP $PRPcurr -PRPS $PRPS -PNP $PNP ${V} > ${LOGDIR}run_combine_1D_${A}_${CHF}_${T}_${WC}_${VF}.txt 2>&1 &

        # python3 1D_scan/run_combine_1D.py -c $channel -w ${WC} -t ${T} -s _1D -p 0.01 -pc 0.05 -U y -a ${AS} -T y ${V} > ${LOGDIR}run_combine_1D_${A}_${CHF}_${T}_${WC}_${VF}.txt 2>&1 &

        # python3 1D_scan/run_combine_1D.py -w FT0 -t f -s _1D -U y -a n -T y -J n -UP y -PRP 4 -PRPS n -PNP y
    done
done < <(python3 -c "
import sys
sys.path.append('${VDICT_DIR}')
from CONFIG_VERSIONS import versions_dict
# for ch, meta in versions_dict.items():
for i, tup in enumerate(sorted(versions_dict.items())):
    ch, meta = tup
    if ${TB}: # if full analysis, only use one channel
        if i > 0:
            continue
    #print '%s %s' % (ch, meta[\"v\"])
    print('%s %s' % (ch, meta[\"v\"]))
")
