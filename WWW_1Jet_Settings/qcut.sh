#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
YEAR=2018
NTHREADS=1 #8 default

while getopts "h?y:s:n:o:a:l:x:q:b:dcp:f" opt; do
    case "$opt" in
    h|\?)
        echo 'triboson-production -y YEAR -s SAMPLE -n NEVENTS -o OUTPUT_DIR -p PILEUP_FILES [-d -c] -a NPART -l LEPTONFILTER 

If the -d (dry run) flag is set, only the environment and the config file will be created.
otherwise, the cmsRun command will be executed.

The -c flag enables the cleanup of temporary directories in the end, which is recommended for
large scale production to save space.

PILEUP_FILES needs to be a file in which the the pileup files are listed, separated by newlines.
You can get this list with the dasgoclient:
    dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" > pileup_files.txt'
        exit 0
        ;;
    y)  YEAR=$OPTARG
        # e.g. 2016, 2017, 2018
        ;;
    s)  SAMPLE=$OPTARG
        # e.g. WWZ_dim8, WZZ_dim8, WWZ_dim8 or ZZZ_dim8
        ;;
    d)  DRY_RUN=1
        # cleanup temporary files in the end, recommended for large scale production
        ;;
    c)  CLEANUP=1
        # Only setup but exit script before actually running cmsRun
        ;;
    o)  OUTPUT_DIR=$OPTARG
        # Output directory of this production
        ;;
    n)  NEVENTS=$OPTARG
        ;;
    a)  NPART=$OPTARG
        ;;
    l)  LEPTONFILTER=$OPTARG
        ;;
    b)  SEED=$OPTARG
        ;;
    x)  XQCUT=$OPTARG
        ;;
    q)  QCUT=$OPTARG
        ;;
    f)  CopyToEos=1 # to copy the outfile to cmslpc eos space
        ;;
    esac
done

echo 'XQCUT=' 
echo ${XQCUT}
echo 'QCUT=' 
echo ${QCUT}
echo 'LEPTONFILTER=' 
echo ${LEPTONFILTER}

shift $((OPTIND-1))

if [ -z "$NEVENTS" ]
then
      echo "-n NEVENTS not specified!"
      exit 1
fi

case "$YEAR" in

2016)  echo "The year $YEAR is not supported!"
    CONDITIONS=80X_mcRun2_asymptotic_2016_TrancheIV_v8
    BEAMSPOT=Realistic50ns13TeVCollision # yes, 50 ns is not correct but this is also used in official 2016 MC productions
    exit 1
    ;;
2017)  echo "The year $YEAR is not supported!"
    CONDITIONS=94X_mc2017_realistic_v17
    BEAMSPOT=Realistic25ns13TeVEarly2017Collision
    exit 1
    ;;
2018)  echo "The year is $YEAR"
    CAMPAIGN=RunIISummer20UL18
    ERA=Run2_2018
    NANOERA=Run2_2018,run2_nanoAOD_106Xv2
    CONDITIONS=106X_upgrade2018_realistic_v4
    CONDITIONS_SIM=106X_upgrade2018_realistic_v11_L1v1
    CONDITIONS_HLT=102X_upgrade2018_realistic_v15
    CONDITIONS_MINIAOD=106X_upgrade2018_realistic_v16_L1v1
    BEAMSPOT=Realistic25ns13TeVEarly2018Collision
    HLTSTEP=2018v32
    ;;
*) echo "Year $YEAR is not valid, did you forget to specify it with the -y option?"
   exit 1
   ;;
esac

if [ "$DRY_RUN" ]
then
      echo "Script will be exited after config file is generated"
else
      echo "The full script will be run, including the cmsRun command and cleaning on the directory"
      if [ "$CLEANUP" ]
      then
            echo "Temporary files and directories will be cleaned up after script is finished"
      else
            echo "No files and directories will be cleaned up in the end,"
            echo "which is not recommended for large scale production (consider setting the -c flag)."
      fi
fi



# The following part should not be manually configured
FRAGMENT_BASE_URL=http://nuhep.northwestern.edu/~sapta/Qcut_1Jet/
GRIDPACK_BASE_URL=http://nuhep.northwestern.edu/~sapta/Qcut_WWW/

FRAGMENT=wmLHEGS-fragment-${YEAR}_${LEPTONFILTER}.py
GRIDPACK=${SAMPLE}_xqcut${XQCUT}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz

STEP0_NAME=${SAMPLE}-${CAMPAIGN}wmLHEGEN_${NPART}_xqcut${XQCUT}_qcut${QCUT}
STEP1_NAME=${SAMPLE}-${CAMPAIGN}SIM_${NPART}_xqcut${XQCUT}_qcut${QCUT}

curl -s --insecure $GRIDPACK_BASE_URL/$GRIDPACK --retry 2 --create-dirs -o $GRIDPACK
if [ -s $GRIDPACK ]
then
  echo "get $GRIDPACK"
else
  echo "can not get $GRIDPACK_BASE_URL/$GRIDPACK"
  echo "curl -s --insecure $GRIDPACK_BASE_URL/$GRIDPACK --retry 2 --create-dirs -o $GRIDPACK"
  exit $?;
fi

# ============= GEN,LHE ==============
# ============= GEN,LHE ==============
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_19_patch3/src ] ; then
  echo release CMSSW_10_6_19_patch3 already exists
else
  scram p CMSSW CMSSW_10_6_19_patch3
fi
cd CMSSW_10_6_19_patch3/src
eval `scram runtime -sh`

curl -s --insecure $FRAGMENT_BASE_URL/$FRAGMENT --retry 2 --create-dirs -o Configuration/GenProduction/python/$FRAGMENT
if [ -s Configuration/GenProduction/python/$FRAGMENT ]
then
  echo "get $FRAGMENT"
else
  echo "can not get $FRAGMENT"
  exit $?;
fi

scram b -j8
cd ../../

#insert gridpack path info fragment
PWDESC=$(echo $PWD | sed 's_/_\\/_g')
sed -i "s/\$GRIDPACK/$PWDESC\/$GRIDPACK/g" $CMSSW_VERSION/src/Configuration/GenProduction/python/$FRAGMENT
sed -i "s/\$QCUT/$QCUT/g" $CMSSW_VERSION/src/Configuration/GenProduction/python/$FRAGMENT


seed=$SEED

cmsDriver.py Configuration/GenProduction/python/$FRAGMENT \
    --python_filename ${STEP0_NAME}_cfg.py \
    --fileout file:${STEP0_NAME}.root \
    --mc \
    --eventcontent RAWSIM,LHE \
    --datatier GEN,LHE \
    --conditions $CONDITIONS \
    --beamspot $BEAMSPOT \
    --step LHE,GEN \
    --geometry DB:Extended \
    --nThreads $NTHREADS \
    --era $ERA \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${seed})" \
    -n $NEVENTS

cmsRun ${STEP0_NAME}_cfg.py
# ============= GEN,LHE ==============
# ============= GEN,LHE ==============

# ============= SIM ==============
# ============= SIM ==============

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

scram b -j4
cd ../..

cmsDriver.py \
  --python_filename ${STEP1_NAME}_cfg.py \
  --eventcontent RAWSIM \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier GEN-SIM \
  --fileout file:${STEP1_NAME}.root \
  --conditions $CONDITIONS_SIM \
  --beamspot $BEAMSPOT \
  --step SIM \
  --geometry DB:Extended \
  --filein file:${STEP0_NAME}.root \
  --era $ERA \
  --runUnscheduled \
  --no_exec \
  --mc \
  -n $NEVENTS

cmsRun ${STEP1_NAME}_cfg.py
# ============= SIM ==============
# ============= SIM ==============

if [ "$DRY_RUN" ]
then
      exit 1
fi
