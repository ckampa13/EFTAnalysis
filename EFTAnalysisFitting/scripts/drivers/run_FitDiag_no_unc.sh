THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/FitDiag/'
OUTDIR=$SCRIPT_DIR'/../../unblind/output/full_analysis/'
echo "LOGDIR=${LOGDIR}"

echo "cd ${OUTDIR}"
cd ${OUTDIR}

echo "Unblinded, no shape uncertainty evaluation"
echo "combine -M FitDiagnostics /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2.0,2.0 --verbose -1 -n _Data_FitDiag_Test --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT --saveShapes --saveOverallShapes > ${LOGDIR}FitDiag_full_analysis_comb_no_unc.txt 2>&1 &"

combine -M FitDiagnostics /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-2.0,2.0 --verbose -1 -n _Data_FitDiag_Test --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT --saveShapes --saveOverallShapes > ${LOGDIR}FitDiag_full_analysis_comb_no_unc.txt 2>&1 &

echo "cd ${THIS_DIR}"
cd ${THIS_DIR}
