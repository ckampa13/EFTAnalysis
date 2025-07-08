#!/bin/bash
. drivers/unblind_run_combine_1D_all.sh Asimov FT0 f n
sleep 0.5
. drivers/unblind_run_combine_1D_all.sh Data FT0 f n
# sleep 0.5
# . drivers/unblind_run_combine_1D_all.sh Asimov FT0 c n
# sleep 0.5
# . drivers/unblind_run_combine_1D_all.sh Data FT0 c n
