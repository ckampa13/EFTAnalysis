#!/bin/sh
ulimit -s unlimited
set -e
cd /uscms_data/d3/ckampa/CMSSW_14_1_0_pre4/src
export SCRAM_ARCH=el9_amd64_gcc12
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd /uscms/home/ckampa/nobackup/EFTAnalysis/EFTAnalysisFitting/scripts

if [ $1 -eq 0 ]; then
  combine --alignEdges 1 COMBINE_OPTIONS -M MultiDimFit --algo grid -d WSFILE --points 30 --firstPoint 0 --lastPoint 9 -n .Test.POINTS.0.9
fi
if [ $1 -eq 1 ]; then
  combine --alignEdges 1 COMBINE_OPTIONS -M MultiDimFit --algo grid -d WSFILE --points 30 --firstPoint 10 --lastPoint 19 -n .Test.POINTS.10.19
fi
if [ $1 -eq 2 ]; then
  combine --alignEdges 1 COMBINE_OPTIONS -M MultiDimFit --algo grid -d WSFILE --points 30 --firstPoint 20 --lastPoint 29 -n .Test.POINTS.20.29
fi

