#!/usr/bin/bash

THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/'
OUTDIR=$SCRIPT_DIR'/../../unblind/output/full_analysis/'
echo "LOGDIR=${LOGDIR}"

echo "cd ${OUTDIR}"
cd ${OUTDIR}

echo "Calculating GoF for data (full analysis)."
echo "combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Data.all_comb.GoF.vCONFIG_VERSIONS > ${LOGDIR}GoF_data_full_analysis_comb.txt 2>&1 &"
combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Data.all_comb.GoF.vCONFIG_VERSIONS > ${LOGDIR}GoF_data_full_analysis_comb.txt 2>&1 &

#combine -M GoodnessOfFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=saturated --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHl3,k_cHbox,k_cHDD,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2,2 --verbose 1 -n _Toys1000_${i}.all_comb.GoF.vCONFIG_VERSIONS --toys 100 --seed=${SEEDS[i]} > ${LOGDIR}GoF_full_analysis_comb_toys_1000_${i}_SEED_${SEEDS[i]}.txt 2>&1 &

echo "cd ${THIS_DIR}"
cd ${THIS_DIR}
