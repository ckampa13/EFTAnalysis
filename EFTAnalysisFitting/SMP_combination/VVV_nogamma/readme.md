# VVV (no $\gamma$)
## What's included
- Yields for full Run 2 for the various channels. Channels are defined based on the number of leptons in the final state.
- 12 dim6 WCs: cW, cHbox, cHDD, cHl3, cHq1, cHq3, cHW, cHWB, cll1, cHB, cHu, cHd
- A single datacard points to all the appropriate shape files, and contains information for all WCs listed above: `VVV.all_combined.dim6_All.DataCard_Yields.vCONFIG_VERSIONS.txt`
	- Analysis has not fully implemented the multi-WC parameterization. The current version artificially sets the "mixed" terms to zero (e.g. `h_sm_lin_quad_mixed_cW_cHbox`).
- EFT model: AnalyticAnomalousCoupling, using the `AnaliticAnomalousCouplingEFTNegative` physics model.
- In the current version, all systematics are assumed to be fully correlated, i.e. they are to be used as directly recorded in the datacard.
- To avoid runtime errors with combine when running stat. only combinations, we artificially add a negligble systematic, `statonly`, which applies an `lnN` scale of value 1.0001 to all processes. Additionally, two nuisance groups are defined: `allsyst` and `nosyst`. Whether running a stat. only combination, or a combination that includes systematics, one should freeze the appropriate nuisance group, i.e. `--freezeNuisanceGroups nosyst` should be used when running the combination with
    systematics.
