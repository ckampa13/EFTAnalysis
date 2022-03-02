#!/bin/bash
#INPUTFILES=${1}.txt
xrdfs root://cmseos.fnal.gov mkdir -p /store/group/lpcvvv/NanoAODv9/${1}
echo ${1}.txt
while IFS= read -r line; do
    echo "$line"
    xrdcp "$line" root://cmseos.fnal.gov///store/group/lpcvvv/NanoAODv9/${1}
done < "${1}.txt"
