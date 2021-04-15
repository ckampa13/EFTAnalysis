
## Relevant operators:

|                    | `WWWW` | `WWZZ` | `ZZZZ`  | 
|--------------------|--------|--------|---------|
| LS0, LS1, LS2      | ✅     | ✅     | ✅      |
| LM0, LM1, LM6, LM7 | ✅     | ✅     | ✅      | 
| LM2, LM3, LM4, LM5 | ❌     | ✅     | ✅      |
| LT0, LT1, LT2      | ✅     | ✅     | ✅      |
| LT5, LT6, LT7      | ❌     | ✅     | ✅      |
| LT8, LT9           | ❌     | ❌     | ✅      | 

## Instructions for sample submission:

#### Create the minimum bias file: 

dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" > pileup_files.txt

## Instructions for a pilot run (will work on UCSD cluster, for other clusters the relevant files need to be copied over):

1. login to ucsd uaf-10 
2. create or mkdir EFTSignalGenerationApr2021
3. cd EFTSignalGenerationApr2021
4. cp /home/users/sapta/public_html/ForLisa/pileup_files.txt .
5. cp /home/users/sapta/public_html/ForLisa/triboson_production.sh .
6. cp /home/users/sapta/public_html/ForLisa/pr.sh .
7. source pr.sh
8. sh triboson_production.sh -p pileup_files.txt -s WWW -c -o $PWD -a 1 -n 10

## Submission of jobs at the LPC cluster:

1. Use the script submitCondorJob.sh
2. To submit several jobs simply use submitCondorJob.sh in a loop as done here: submitJob.sh
3. Update the script triboson_production.sh with the correct url for procuring gridpacks and fragments

## Lepton filters:

#### We plan on submitting jobs in three modes:

1. Nofilter (NoFilter/wmLHEGS-fragment-2018.py)
2. Dilepton (Dilepton/wmLHEGS-fragment-2018.py)
3. FourLepton (FourLepton/wmLHEGS-fragment-2018.py)

## To generate samples with the use of specific filters, please use the version of scripts in this directory: ScriptWithLeptonFilterArg

For running an interactive test, please do:

sh triboson_production.sh -p pileup_files.txt -s WWZ_ScaleST -c -o $PWD -a 1 -l DileptonFilter -n 10

1. For DileptonFilter, -l argument is set to DileptonFilter
2. For DileptonFilter, -l argument is set to FourleptonFilter
3. For inclusive or no lepton filter, -l argument is set to NoFilter

Consistent set of condor scripts should be in ScriptWithLeptonFilterArg and has been tested


## Samples to generate


| Process            | `No filter` | `Two lepton filtered` | `Four lepton filtered`  |   `Events per lepton filter scenario` |
|--------------------|-------------|-----------------------|-------------------------|---------------------------------------|
| WWW                | ✅          | ✅                    | ❌                      |  1M				     |	
| WWZ                | ✅          | ✅                    | ✅                      |  1M				     |
| WZZ                | ✅          | ✅                    | ✅                      |  1M				     |
| ZZZ                | ✅          | ✅                    | ✅                      |  1M				     |

#### Near term goal 

To have the first two rows of production done first.
