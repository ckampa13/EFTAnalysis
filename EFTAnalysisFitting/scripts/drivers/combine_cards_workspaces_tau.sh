#!/usr/bin/bash

# arguments: 2 (optional) -- dim to make workspaces for, e.g. "all" (default), "dim6", "dim8"; NDIM or not, e.g. "" (default), "_NDIM"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/tau/'
echo "LOGDIR=${LOGDIR}"

if [[ -z "$1" ]]; then
    D="all"
else
    D=$1
fi

if [[ -z "$2" ]]; then
    V=""
    VF=""
else
    if [[ "$2" == "" ]]; then
        V=""
        VF=""
    else
        V="-v $2"
        VF=$2
    fi
fi

echo "D=${D}, V=${V}"
echo

echo Combining cards channel level...
echo "python tools/combine_cards.py -U y ${V} > ${LOGDIR}combine_cards${VF}.txt 2>&1"
python tools/combine_cards.py -U y ${V} > ${LOGDIR}combine_cards${VF}.txt 2>&1
echo Combining cards all taus...
echo "python tools/LOO_combine_cards.py -c not_tau -U y ${V} > ${LOGDIR}tau_comb_combine_cards${VF}.txt 2>&1"
python tools/LOO_combine_cards.py -c not_tau -U y ${V} > ${LOGDIR}tau_comb_combine_cards${VF}.txt 2>&1
echo Making workspaces for channel level...
echo "python tools/make_workspaces.py -c 1Lepton_1T -d ${D} -t c -U y ${V} > ${LOGDIR}make_workspaces_1L_1T_${D}${VF}.txt 2>&1 &"
python tools/make_workspaces.py -c 1Lepton_1T -d ${D} -t c -U y ${V} > ${LOGDIR}make_workspaces_1L_1T_${D}${VF}.txt 2>&1 &
echo "python tools/make_workspaces.py -c 2Lepton_1T -d ${D} -t c -U y ${V} > ${LOGDIR}make_workspaces_2L_1T_${D}${VF}.txt 2>&1 &"
python tools/make_workspaces.py -c 2Lepton_1T -d ${D} -t c -U y ${V} > ${LOGDIR}make_workspaces_2L_1T_${D}${VF}.txt 2>&1 &
echo Making workspaces for tau combination...
echo "python tools/LOO_make_workspaces.py -c not_tau -d ${D} -U y ${V} > ${LOGDIR}make_workspaces_tau_comb_${D}${VF}.txt 2>&1 &"
python tools/LOO_make_workspaces.py -c not_tau -d ${D} -U y ${V} > ${LOGDIR}make_workspaces_tau_comb_${D}${VF}.txt 2>&1 &
