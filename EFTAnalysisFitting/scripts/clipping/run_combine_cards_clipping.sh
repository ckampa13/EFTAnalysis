#!/usr/bin/bash

#for i in $(seq 0 12);
#for i in $(seq 0 14); # adding a few points just below 1 TeV
for i in $(seq 0 17); # adding a few points just below 1 TeV
do
    echo Combining cards for clip index $i...
    python tools/combine_cards.py -v _clip_mVVV_$i -d clipping
done
