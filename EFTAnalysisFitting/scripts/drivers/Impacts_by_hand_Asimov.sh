THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/Impacts/'
OUTDIR=$SCRIPT_DIR'/../../unblind/output/full_analysis/'
echo "LOGDIR=${LOGDIR}"

echo "cd ${OUTDIR}"
cd ${OUTDIR}

# which NP, what range
# UPDATE VALUES
NP="norm_WW_"
NP_U=0.8826533075596733
NP_D=-1.0185208353259632
####
# NP="norm_QCD_0L_2FJ_"
# NP_U=-0.0672103321887022
# NP_D=-0.934480797151983

echo "${NP} +1sigma..."
echo "Asimov"
echo "combine -M MultiDimFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root -t -1 --algo=grid --points 202 --alignEdges 1  --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,${NP},k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1,${NP}=${NP_U} --setParameterRanges k_cW=-1.0,1.01 --verbose -1 -n
_Asimov_${NP}_Up_Impact.all_combined.cW_1D.vCONFIG_VERSIONS.syst --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT"

combine -M MultiDimFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root -t -1 --algo=grid --points 202 --alignEdges 1  --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,${NP},k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1,${NP}=${NP_U} --setParameterRanges k_cW=-1.0,1.01 --verbose -1 -n _Asimov_${NP}_Up_Impact.all_combined.cW_1D.vCONFIG_VERSIONS.syst --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT

echo "${NP} -1sigma..."
echo "Asimov"
echo "combine -M MultiDimFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root -t -1 --algo=grid --points 202 --alignEdges 1  --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,${NP},k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1,${NP}=${NP_D} --setParameterRanges k_cW=-1.0,1.01 --verbose -1 -n
_Asimov_${NP}_Down_Impact.all_combined.cW_1D.vCONFIG_VERSIONS.syst --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT"

combine -M MultiDimFit /uscms_data/d3/ckampa/EFTAnalysis/EFTAnalysisFitting/unblind/workspaces/full_analysis/VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root -t -1 --algo=grid --points 202 --alignEdges 1  --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,${NP},k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1,${NP}=${NP_D} --setParameterRanges k_cW=-1.0,1.01 --verbose -1 -n _Asimov_${NP}_Down_Impact.all_combined.cW_1D.vCONFIG_VERSIONS.syst --robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT

echo "cd ${THIS_DIR}"
cd ${THIS_DIR}
