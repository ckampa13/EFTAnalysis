#!/usr/bin/env bash

# vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )


# first, setup cmsenv
cd ${CMSSW_BASE}/src/
cmsenv
# go back to script directory
cd ${SCRIPT_DIR}

# cmdline args
# option for running a single channel
channel="all"
while getopts c: flag
do
    case "${flag}" in
        c) channel=${OPTARG};;
    esac
done

echo "Running on the following channel(s): $channel"

# 0Lepton
CHANNEL="0Lepton"
# if single channel arg, check if this is the channel
if [ "$channel" = "all" ] || [ "$channel" = "$CHANNEL" ]; then
    echo "Channel: $CHANNEL"
    # run command, in a loop
    for bin in 1 2 3
    do
        echo "bin: $bin"
        python3 combine_single_channel_single_bin.py -c ${CHANNEL} -b $bin -v 1 -a y -p 0.001 -pc 0.01 -V 0
    done
fi

# 1Lepton
CHANNEL="1Lepton"
# if single channel arg, check if this is the channel
if [ "$channel" = "all" ] || [ "$channel" = "$CHANNEL" ]; then
    echo "Channel: $CHANNEL"
    # run command, in a loop
    for subch in _electron _muon
    do
        echo "Subchannel: $subch"
        for bin in 1 2 3 4
        do
            echo "bin: $bin"
            python3 combine_single_channel_single_bin.py -c ${CHANNEL} -s $subch -b $bin -v 1 -a y -p 0.001 -pc 0.01 -V 0
        done
    done
fi

# 2OSLepton
CHANNEL="2OSLepton"
# if single channel arg, check if this is the channel
if [ "$channel" = "all" ] || [ "$channel" = "$CHANNEL" ]; then
    echo "Channel: $CHANNEL"
    # run command, in a loop
    for subch in _OF
    do
        echo "Subchannel: $subch"
        for bin in 1 2 3
        do
            echo "bin: $bin"
            python3 combine_single_channel_single_bin.py -c ${CHANNEL} -s $subch -b $bin -v 1 -a y -p 0.001 -pc 0.01 -V 0
        done
    done
fi

# 2SSLepton
CHANNEL="2SSLepton"
# if single channel arg, check if this is the channel
if [ "$channel" = "all" ] || [ "$channel" = "$CHANNEL" ]; then
    echo "Channel: $CHANNEL"
    # run command, in a loop
    for bin in 1 2 3
    do
        echo "bin: $bin"
        python3 combine_single_channel_single_bin.py -c ${CHANNEL} -s 1Jet -b $bin -v 1 -a y -p 0.001 -pc 0.01 -V 0
    done
fi
