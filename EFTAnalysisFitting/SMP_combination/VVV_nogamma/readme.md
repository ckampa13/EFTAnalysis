# VVV (no $\gamma$)
## What's included
- Yields for full Run 2 for the various channels. Channels are defined based on the number of leptons in the final state.
- 12 dim6 WCs: cW, cHbox, cHDD, cHl3, cHq1, cHq3, cHW, cHWB, cll1, cHB, cHu, cHd
- A single datacard points to all the appropriate shape files, and contains information for all WCs listed above: `VVV.all_combined.dim6_All.DataCard_Yields.vCONFIG_VERSIONS.txt`
	- Analysis has not fully implemented the multi-WC parameterization. The current version artificially sets the "mixed" terms to zero (e.g. `h_sm_lin_quad_mixed_cW_cHbox`).
- EFT model: AnalyticAnomalousCoupling, using the `AnaliticAnomalousCouplingEFTNegative` physics model.
- To avoid runtime errors with combine when running stat. only combinations, we artificially add a negligble systematic, `statonly`, which applies an `lnN` scale of value 1.0001 to all processes. Additionally, two nuisance groups are defined: `allsyst` and `nosyst`. Whether running a stat. only combination, or a combination that includes systematics, one should freeze the appropriate nuisance group, i.e. `--freezeNuisanceGroups nosyst` should be used when running the combination with
    systematics.

## Timeline of updates
- Apr 9, 2024:
	- Channels: 0Lepton_2FJ, 0Lepton_3FJ, 1Lepton, 2Lepton_OS, 2Lepton_SS
	- Systematics: Background systematics (mostly complete), some signal systematics
- Sep 8, 2024:
	- Channels: 0Lepton_2FJ, 0Lepton_3FJ, 1Lepton, 2Lepton_OS, 2Lepton_SS, 2Lepton_OS_2FJ, 0Lepton_1T, 1Lepton_1T, 2Lepton_1T
		- 2Lepton_OS_2FJ and three tau channels (0Lepton_1T, 1Lepton_1T, 2Lepton_1T) added.
	- Systematics: all background systematics, all signal systematics.
		- Lepton SFs (el and mu) are treated as 50% correlated between each subchannel. This is accomplished using Cholesky decomposition, and the original SF NP is split into N NP, where N is the number of channels that are affected by that systematic (e.g. for el, "lep_sf_el_" --> ["lep_sf_el_1_", "lep_sf_el_2_",...,"lep_sf_el_8_"])
		- There may be minor changes to the systematics in the future; this is expected to have a small impact on the limits.
		- Tau channels use a conservative 50% flat systematic uncertainty for each background process. These will be refined soon.
		- Tau channels have limited signal systematics; they are under development right now.
	- Other notable changes: all channels include fatjet SFs. All channels except 0Lepton_2FJ, 0Lepton_3FJ, and all tau channels use pT dependent fatjet SFs. The inclusion of fatjet SFs leads to a degradation of limits. There is a small difference between pT dependent and pT independent fatjet SFs.
