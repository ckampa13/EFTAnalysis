#!/bin/bash
cwd=$(pwd)
cd ~/nobackup/CMSSW_10_2_13/src
cmsenv
cd $cwd

# make workspace
text2workspace.py VVV_nogamma/VVV.all_combined.dim6_All.DataCard_Yields.vCONFIG_VERSIONS.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative -o VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --X-allow-no-signal --PO eftOperators=cW,cHbox,cHDD,cHl3,cHq1,cHq3,cHW,cHWB,cll1,cHB,cHu,cHd

# run combine on cW, freezing all other WCs
combine -M MultiDimFit VVV.all_combined.dim6_All.workspace.vCONFIG_VERSIONS.root --algo=grid --points 21 --alignEdges 1 -t -1 --redefineSignalPOIs k_cW --freezeNuisanceGroups nosyst --freezeParameters r,k_cHbox,k_cHDD,k_cHl3,k_cHq1,k_cHq3,k_cHW,k_cHWB,k_cll1,k_cHB,k_cHu,k_cHd --setParameters r=1 --setParameterRanges k_cW=-0.5,0.5 --verbose -1 -n _VVV_nogamma_cW_1D

# print limits
python print_limits.py
