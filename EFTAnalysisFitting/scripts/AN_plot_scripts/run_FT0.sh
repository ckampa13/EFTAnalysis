#!/bin/bash
python NLL_limits_plot_from_dir.py -w FT0 -t f -s _1D -l y -U y -a y
python NLL_limits_plot_from_dir.py -w FT0 -t f -s _1D -l y -U y -a n
#python NLL_limits_plot_from_dir.py -c 1Lepton -w FT0 -t c -s _1D -l y -U y -a y
#python NLL_limits_plot_from_dir.py -c 1Lepton -w FT0 -t c -s _1D -l y -U y -a n
#python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -w FT0 -t c -s _1D -l y -U y -a y
#python NLL_limits_plot_from_dir.py -c 0Lepton_3FJ -w FT0 -t c -s _1D -l y -U y -a n
python summary_NLL_limits_plot.py -w FT0 -U y -a y -OD n
python summary_NLL_limits_plot.py -w FT0 -U y -a y -OD y
python summary_NLL_limits_plot.py -w FT0 -U y -a n -OD n
