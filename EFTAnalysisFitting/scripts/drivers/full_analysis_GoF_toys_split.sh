#!/usr/bin/bash

# arguments: 3 (optional) -- WC (e.g. "cW" for testing, dim6, all); "_1D" (default) or "_All" (freeze vs. profile); NDIM or not, e.g. "" (default), "_NDIM"
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
# blind
# LOGDIR=$SCRIPT_DIR'/../../output/logs/toys/'
# OUTDIR=$SCRIPT_DIR'/../../output/full_analysis/'
# unblind
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/toys/'
OUTDIR=$SCRIPT_DIR'/../../unblind/output/full_analysis/'
echo "LOGDIR=${LOGDIR}"

# if [[ -z "$1" ]]; then
#     WC="cW"
# else
#     WC=$1
# fi

# if [[ -z "$2" ]]; then
#     S="_1D"
# else
#     S=$2
# fi

# if [[ -z "$3" ]]; then
#     V=""
#     VF=""
# else
#     if [[ "$3" == "" ]]; then
#         V=""
#         VF=""
#     else
#         V="-v $3"
#         VF=$3
#     fi
# fi

# echo "WC=${WC}, V=${V}"
# echo

SEEDS=(100 200 300 400 500 600 700 800 900 1000)
length=${#SEEDS[@]}

echo "cd ${OUTDIR}"
cd ${OUTDIR}

for ((i=0; i<length; i++)); do
    echo "Iteration ${i}: SEED=${SEEDS[i]}"
    # blind
    # echo "Blinded"
    # echo "combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Toys1000_${i}.all_comb.GoF.vCONFIG_VERSIONS --toys 100 --seed=${SEEDS[i]} > ${LOGDIR}GoF_full_analysis_comb_toys_1000_${i}_SEED_${SEEDS[i]}.txt 2>&1 &"
    # combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Toys1000_${i}.all_comb.GoF.vCONFIG_VERSIONS --toys 100 --seed=${SEEDS[i]} > ${LOGDIR}GoF_full_analysis_comb_toys_1000_${i}_SEED_${SEEDS[i]}.txt 2>&1 &
    # unblind
    echo "Unblinded"
    echo "combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Toys1000_${i}.all_comb.GoF.vCONFIG_VERSIONS --toys 100 --seed=${SEEDS[i]} > ${LOGDIR}GoF_full_analysis_comb_toys_1000_${i}_SEED_${SEEDS[i]}.txt 2>&1 &"
    combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Toys1000_${i}.all_comb.GoF.vCONFIG_VERSIONS --toys 100 --seed=${SEEDS[i]} > ${LOGDIR}GoF_full_analysis_comb_toys_1000_${i}_SEED_${SEEDS[i]}.txt 2>&1 &
done

echo "cd ${THIS_DIR}"
cd ${THIS_DIR}
