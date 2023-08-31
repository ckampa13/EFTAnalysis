# CMS VVV Higgs combine Tools

The CMS VVV analysis group uses Higgs combine and AnalyticAnomalousCoupling to set limits on Wilson coefficients.

## 1. Installation
These instructions are for installation on the LPC. Cole's installation is on `~/nobackup/`, but installation from any user directory should be fine. Installation was last tested on August 31, 2023.

### a) CMSSW
```
cd ~/nobackup
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
```
### b) Higgs combine
```
cd ~/nobackup/CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.1.0
```

### c) AnalyticAnomalousCoupling
```
cd ~/nobackup/CMSSW_10_2_13/src/HiggsAnalysis
git clone https://github.com/amassiro/AnalyticAnomalousCoupling.git
scramv1 b clean; scramv1 b # always make a clean build
```

Note the scram build step will take several minutes.

### d) VVV analysis codes
The current recommendation is to fork from Sapta's repository. Please use the clone link for your fork (replace: ckampa13 with your GitHub username).
```
cd ~/nobackup

git clone https://github.com/ckampa13/EFTAnalysis.git
cd EFTAnalysis
git remote add upstream https://github.com/Saptaparna/EFTAnalysis.git
```

## 2. Basic Running
Before running, be sure that `cmsenv` has been run from the appropriate location (e.g. `~/nobackup/CMSSW_10_2_13/src/`)

DataCards and yield files are stored in `EFTAnalysis/EFTAnalysisFitting` in subdirectories for each channel. This directory is referred to here and in the code as `datacard_dir`. Within each channel subdirectory, there are subdirectories for each version of the yields, as well as a `raw_yields` directory where original yield files are stored for processing.

All commands should be run from the following directory: `~/nobackup/EFTAnalysis/EFTAnalysisFitting/scripts`. Any following references to `scripts/` is a reference to this directory.

There are several configuration files in `scripts/`. The two which may need to be changed are:
- `scripts/DATACARD_DICT.py`: for updating binning
- `scripts/CONFIG_VERSIONS.py`: for updating version number, available WCs, and input type (point scan vs. parameters) for each channel

There are five steps to running the combination. As an example, we will consider the case that you wish to rerun the combination for the 0 Lepton 2 FatJet channel:
### a) Process the yield ROOT file and generate DataCards
- Copy yield file into channel's `raw_yields` directory:
  - e.g. `cp VVV.0L_2F.DataCard_Yields.v1000.root ~/nobackup/EFTAnalysis/EFTAnalysisFitting/0Lepton_2FJ/raw_yields/`
- Update relevant configuration files:
  - `scripts/CONFIG_VERSIONS.py`
    - Update `versions_dict['0Lepton_2FJ']['v']` to the appropriate version label.
      - e.g. `'v': '1000'` for the yield file above.
    - It is assumed the VVV yield dependence is stored in the yield file as a set of histograms at different EFT set points. If this is the case, `versions_dict['0Lepton_2FJ']['EFT_type']` should be set to 'points'. Note the 'params' option is not currently implemented.
    - If the Wilson coefficients available in the yield file have changed, please update the list `versions_dict['0Lepton_2FJ']['EFT_ops']`, making sure to use the name strings exactly as shown in `WC_ALL` at the bottom of the file.
  - `scripts/DATACARD_DICT.py`: if the number of bins is changing, update `datacard_dict['0Lepton_2FJ']['subchannels']['']['bins']` (and any other subchannels if needed) to include an index for each bin (starting index of 1). **FIXME! It would be better to parse this directly from the yield files.**
- Run the processing script:
```
[scripts]$ python datacards/make_1D_scan_datacards.py -c 0Lepton_2FJ -v v1000
```


### b) Split yields to individual bins, and generate single bin DataCards
This step is required only if you wish to run combine at the bin level. If the `-c` command-line argument is not included, the yields will be split for all channels.
```
[scripts]$ python tools/split_yields.py -c 0Lepton_2FJ
```

### c) Combine DataCards
This step is required only if you wish to run combine at the channel combination or full analysis combination level. If the `-c` command-line argument is not included, DataCards will be combined for all channels. If the `-w` command-line argument is not included, DataCards for all Wilson coefficients defined in the `WC_ALL` list (`scripts/CONFIG_VERSIONS.py`) will be combined.
```
[scripts]$ python tools/combine_cards.py -c 0Lepton_2FJ
```

### d) Make workspaces
The RooWorkspace is fed into combine for doing the NLL vs. WC scan. If the `-c` command-line argument is not included, workspaces will be generated for all channels. The `-t` command-line argument is used to specify which level of the analysis to generate the workspaces (default is all levels) -- `b` (bin) `s` (subchannel) `c` (channel) `f` (full analysis) can be included in any order. For the example below, all but the full analysis are included.
```
[scripts]$ python tools/make_workspaces.py -c 0Lepton_2FJ -t bsc
```

### e) Run combine
If the `-c` command-line argument is not included, combine will be run for all channels. If the `-w` command-line argument is not included, combine will be run for all Wilson coefficients defined in the `WC_ALL` list (`scripts/CONFIG_VERSIONS.py`). The `-t` command-line argument is used to specify which level of the analysis to run combine on (default is all levels) -- `b` (bin) `s` (subchannel) `c` (channel) `f` (full analysis) can be included in any order. For the example below, all but the full analysis are included.
```
[scripts]$ python 1D_scan/run_combine_1D.py -c 0Lepton_2FJ -t bsc
```

The output is stored in `datacard_dir/output/` in several subdirectories:
- `single_bin` : results for bin level analysis
- `subchannel` : results for subchannel level analysis
- `channel` : results for channel level analysis
- `full_analysis` : results for full analysis

The output files have the following name format: `higgsCombine_Asimov.${CHANNEL}${SUBCHANNEL}${BINLABEL}.${WC}_1D.v${VERSION}.${SYSTLABEL}.MultiDimFit.mH120.root`
with the following keys:
- ${CHANNEL}: short name (e.g. `0L_2FJ`) of the channel, or `all` for full analysis.
- ${SUBCHANNEL}: short name (e.g. '') of the subchannel. `_combined` is appended for the channel level and full analysis.
- ${BINLABEL}: empty string except for the bin level analysis, then filled with `_bin#` where `#` is the bin number (first bin is 1).
- ${WC}: Wilson coefficient in the scan, e.g. `cW`
- ${VERSION}: for bin, subchannel, and channel, this is the yield version (see `versions_dict` in `scripts/CONFIG_VERSION.py`). For the full analysis, $(VERSION)=`CONFIG_VERSIONS`, as each channel may be at a different version.
- ${SYSTLABEL}: `syst` for calculation including systematics, `nosyst` for calculation that includes statistical uncertainty only.

Within each output file, the following leaves from the `limit` tree can be used to extract limits:
- `k_${WC}` (e.g. `k_cW`) stores the values of the WC at each point in the scan
- `deltaNLL` stores the deltaNLL values at each point in the scan.
