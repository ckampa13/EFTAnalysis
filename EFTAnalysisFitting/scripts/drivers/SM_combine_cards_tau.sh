#!/usr/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
LOGDIR=$SCRIPT_DIR'/../../unblind/output/logs/tau/'
echo "LOGDIR=${LOGDIR}"

echo Combining SM cards channel level...
echo "python tools/SM_combine_cards.py -U y > ${LOGDIR}SM_combine_cards.txt 2>&1"
python tools/SM_combine_cards.py -U y > ${LOGDIR}SM_combine_cards.txt 2>&1
echo Combining SM cards all taus...
echo "python tools/LOO_SM_combine_cards.py -c not_tau -U y > ${LOGDIR}SM_tau_comb_combine_cards.txt 2>&1"
python tools/LOO_SM_combine_cards.py -c not_tau -U y > ${LOGDIR}SM_tau_comb_combine_cards.txt 2>&1
