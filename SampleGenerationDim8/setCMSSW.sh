CMSSW_VERSION=CMSSW_10_2_22
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW $CMSSW_VERSION
tar -zcvf CMSSW_10_2_22.tar.gz CMSSW_10_2_22 
