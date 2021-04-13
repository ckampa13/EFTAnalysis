
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

## Submission of jobs at the LPC cluster:

1. Use the script submitCondorJob.sh
2. To submit several jobs simply use submitCondorJob.sh in a loop as done here: submitJob.sh

## Lepton filters:

#### We plan on submitting jobs in three modes:

1. Nofilter (NoFilter/wmLHEGS-fragment-2018.py)
2. Dilepton (Dilepton/wmLHEGS-fragment-2018.py)
3. FourLepton (FourLepton/wmLHEGS-fragment-2018.py)

 
