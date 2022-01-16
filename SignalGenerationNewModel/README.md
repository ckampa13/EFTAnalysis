
## Relevant operators:

|                              | `WWWW` | `WWZZ` | `ZZZZ`  | 
|------------------------------|--------|--------|---------|
| LS0, LS1, LS2                | ✅     | ✅     | ✅      |
| LM0, LM1, LM6, LM7           | ✅     | ✅     | ✅      | 
| LM2, LM3, LM4, LM5           | ❌     | ✅     | ✅      |
| LT0, LT1, LT2                | ✅     | ✅     | ✅      |
| LT3, LT4, LT5, LT6, LT7      | ❌     | ✅     | ✅      |
| LT8, LT9                     | ❌     | ❌     | ✅      | 

## Instructions for sample submission:

#### Create the minimum bias file: 

dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" > pileup_files.txt

It can also be produced by running [pr.sh][https://github.com/Saptaparna/EFTAnalysis/blob/master/SignalGenerationNewModel/pr.sh] 


## Submission of jobs at the LPC cluster:

1. Use the script submitCondorJob.sh
2. To submit several jobs simply use submitCondorJob.sh in a loop as done here: submitJob.sh
3. Update the script triboson_production.sh with the correct url for procuring gridpacks and fragments
4. When copying to eos, update with the correct destination directory

## Lepton filters:

#### We plan on submitting jobs in three modes:

1. Nofilter (NoFilter/wmLHEGS-fragment-2018.py)
2. Dilepton (Dilepton/wmLHEGS-fragment-2018.py)
3. FourLepton (FourLepton/wmLHEGS-fragment-2018.py)

## For running an interactive test, please do:

sh triboson_production.sh -p pileup_files.txt -s WWW -c -o $PWD -a 1 -n 10 -b 12345 -l NoFilter 

1. For DileptonFilter, -l argument is set to DileptonFilter
2. For DileptonFilter, -l argument is set to FourleptonFilter
3. For inclusive or no lepton filter, -l argument is set to NoFilter


## Samples to generate


| Process            | `No filter` | `Two lepton filtered` | `Four lepton filtered`  |   `Events per lepton filter scenario` |
|--------------------|-------------|-----------------------|-------------------------|---------------------------------------|
| WWW                | ✅          | ✅                    | ❌                      |  1M				     |	
| WWZ                | ✅          | ✅                    | ✅                      |  1M				     |
| WZZ                | ✅          | ✅                    | ✅                      |  1M				     |
| ZZZ                | ✅          | ✅                    | ✅                      |  1M				     |

