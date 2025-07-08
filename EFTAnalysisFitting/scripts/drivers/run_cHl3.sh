#!/bin/bash
. drivers/unblind_run_combine_1D_all.sh Asimov cHl3 f n
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Data cHl3 f n
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Asimov cHl3 f n _NDIM
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Data cHl3 f n _NDIM
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Asimov cHl3 c n
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Data cHl3 c n
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Asimov cHl3 c n _NDIM
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Data cHl3 c n _NDIM
