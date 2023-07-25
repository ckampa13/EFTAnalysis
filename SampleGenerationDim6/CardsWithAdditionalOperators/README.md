
## Relevant operators:

|                    | `WWWW` | `WWZZ` | `ZZZZ`  | 
|--------------------|--------|--------|---------|
| cW                 | ✅     | ✅     | ❌      |
| cHW                | ✅     | ✅     | ✅      | 
| cHWB               | ✅     | ✅     | ✅      |
| cHDD               | ✅     | ✅     | ✅      |
| cB                 | ❌     | ❌     | ✅      |
| cHq1               | ✅     | ✅     | ✅      |
| cHq3               | ✅     | ✅     | ✅      |
| cHl3               | ✅     | ✅     | ✅      |
| cll1               | ✅     | ✅     | ✅      |
| cHu                | ❌     | ✅     | ✅      |
| cHd                | ❌     | ✅     | ✅      |

## Instructions for sample submission:

### Create the minimum bias file: 

dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" > pileup_files.txt

### Running the production script

All code for the production can be found under the JobSubmission directory

There are several scripts in that directory

- pr.sh: sets proxy for job
- submitCondorJob.sh: condor job configuration and arguments are specified
- submitJob.sh: submitting the job, which entails running submitCondorJob.sh in a loop
- triboson_production.sh: the actual script that will be run on the worker nodes 

## Submission of jobs at the LPC cluster:

1. Use the script submitCondorJob.sh
2. To submit several jobs simply use submitCondorJob.sh in a loop as done here: submitJob.sh
3. Update the script triboson_production.sh with the correct url for procuring gridpacks and fragments
4. Do not submit Nofilter and DileptonFilter jobs from one directory, while this is fixed in the newest iteration so the jobs are not overwritten, it is easier for book-keeping to keep submission separate
5. If submitting jobs at the LPC, please use your nobackup area (/uscms/home/${USERNAME}/nobackup/), submitting from home may clog up the home area
6. If you want to keep local copies of the files, then please remove these lines in the `triboson_production.sh` script:
- https://github.com/Saptaparna/EFTAnalysis/blob/master/SampleGenerationDim6/CardsWithAdditionalOperators/JobSubmission/triboson_production.sh#L476ToL477 

## Lepton filters:

#### We plan on submitting jobs in two modes:

1. Nofilter (NoFilter/wmLHEGS-fragment-2018.py)
2. Dilepton (Dilepton/wmLHEGS-fragment-2018.py)

## To generate samples with the use of specific filters, please use the version of scripts in this directory: 

For running an interactive test, please do:

sh triboson_production.sh -p pileup_files.txt -s ZZZ_1Jet_xqcut15_12Operators_4F -c -o $PWD -a 1 -n 10 -b 12345 -l NoFilter -f

1. For DileptonFilter, -l argument is set to DileptonFilter

## Samples to generate


| Process            | `No filter` | `Two lepton filtered` |   `Events per lepton filter scenario` |
|--------------------|-------------|-----------------------|---------------------------------------|
| WWW                | ✅          | ✅                    |             1M		           |	
| WWZ                | ✅          | ✅                    |             1M	                   |
| WZZ                | ✅          | ✅                    |             1M		           |
| ZZZ                | ✅          | ✅                    |             1M	                   |

## For keeping track of sample production, we have the following spreadsheet:

https://docs.google.com/spreadsheets/d/14xAqp9kCjJNmuxpJDPC7XgNk1O6dF5_KQl-Qo8HMd68/edit#gid=0

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQKFTabgcDU_F7Kv5zzlfi4UFi2rieA4CaLjOS5NHoRPj0i4bg5UVeNujEurKoBGCdOtGe6UP3YAKhY/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false", width=800, height=500></iframe>
