#!/usr/bin/env bash

# vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
CHANNEL="1Lepton"

# first, setup cmsenv
cd ${CMSSW_BASE}/src/
cmsenv
# go back to script directory
cd ${SCRIPT_DIR}

# run command, in a loop
for subch in electron muon
do
    echo "Subchannel: $subch"
    for bin in 1 2 3 4
    do
        echo "bin: $bin"
        python3 combine_single_channel_single_bin.py -c ${CHANNEL} -s $subch -b $bin -v 1 -a y
    done
done
