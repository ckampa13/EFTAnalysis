#!/usr/bin/env bash

# vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )

# first, setup cmsenv, in case it has not been set already
cd ${CMSSW_BASE}/src/
cmsenv
# go back to script directory
cd ${SCRIPT_DIR}

# run command, in a loop
for dir in subchannel channel full_analysis
do
    echo "Datacard directory: combined_datacards/$dir"
    python3 combine_from_dir.py -d combined_datacards/${dir} -a y -p 0.001 -pc 0.01 -V 0
done
