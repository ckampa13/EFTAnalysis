# store version of each channel to use when running combine
# also track what integrated luminosity is in that version of the yield file
versions_dict = {
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHDD', 'cHW', 'cHB', 'cHWB']}, # no systematics
    # '0Lepton_2FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not suppressed.
    # '0Lepton_2FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_2FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_2FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updates.
    # '0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    #'0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    '0Lepton_2FJ': {'v': 18, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 1D complete, with all systematics. Missing VH.
    # '0Lepton_3FJ': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points'},
    # '0Lepton_3FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points'}, # rebinning test, no systematics, more 1D scans
    # '0Lepton_3FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_3FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not supressed.
    # '0Lepton_3FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_3FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_3FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updatees.
    # '0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    #'0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    '0Lepton_3FJ': {'v': 18, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim6 1D complete, with all systematics. Missing VH.
    # '1Lepton': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '1Lepton': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # cW -> VVV+1Jet, all other dim6 added. autoMCStats should be turned off.
    #'1Lepton': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # All dim8 added (dim6 bugged). Processed only FT0, FM0. autoMCStats should be turned off.
    #'1Lepton': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # Signal systematics added for dim6 and dim8 (missing PDF, alpha_s, QCD_scales). All dim8 added. Processed only FT0, FM0. autoMCStats should be turned off.
    '1Lepton': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics. Items to debug (JES and JER removed due to bugs; Vgamma is missing; trigger_weight_ is missing; SM is using EFT scan values)
    # '2Lepton_OS': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params'}, # bin error
    # '2Lepton_OS': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params'},
    #'2Lepton_OS': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # removed WWZ ggH
    # '2Lepton_OS': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # signal xsec bug fix
    # '2Lepton_OS': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # 1Jet sample processed
    # '2Lepton_OS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 completed, with minor errors in point scans (removed points)
    #'2Lepton_OS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8 completed (FT0, FM0), dim6 completed (with bugged points fixed)
    #'2Lepton_OS': {'v': 8, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # lumi bug fixed (dim6 and dim8), dim6 signal systematics added with a few missing (PDF, alpha_s, QCD scales). Background uncertainty for DY updated to alternate method (more conservative)
    #'2Lepton_OS': {'v': 9, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # PDF, QCD scale, lumi uncertainties added for dim6.
    #'2Lepton_OS': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # PDF, QCD scale fixed. dim8 updated for xqcut and +1Jet.
    #'2Lepton_OS': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # tightWtagSF processed. Note new file has different values for nominal, so I subtracted to find contribution, and added to v10 nominal values.
    #'2Lepton_OS': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # processed all signal systematics -- new file format. Includes nominal values, so reprocessing those as well. dim8 copied from v11.
    '2Lepton_OS': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics. Items to debug (SM is using EFT scan values; systematics for cHu removed due to bug)
    # '2Lepton_SS': {'v': 1, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '2Lepton_SS': {'v': 2, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1']}, # only WWW
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # VVV, but only cW -- first batch
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # VVV 1J
    #'2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # VVV 1J, same as previous line with dim8 added.
    #'2Lepton_SS': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim6 signal systematics added with a few missing (PDF, alpha_s, QCD_scales). TTbar updated to data driven (including uncertainty). dim8 missing but added by hand from cleaned v3 file.
    #'2Lepton_SS': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # updated systematics. binning has changed and dim8 still not ready, so removed it from 2L_SS operators. Be aware of this when looking at the results before this is added in again.
    '2Lepton_SS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics.
    # '2Lepton_SS': {'v': 1001, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # TEST!! of Yulun's proposal for EFTfitCoefficient matrix for analysts to report yields. This is supplied for dim6 at the inclusive level of the analysis with dilepton filter. I have rebinned the matrix for sT to look like Yulun's SR binning. I added a single background that roughly corresponds to...
    #'2Lepton_SS': {'v': 1002, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # TEST!! of Yulun's proposal for EFTfitCoefficient matrix for analysts to report yields. This is supplied for dim6 in the signal region. I added a single background that corresponds to...
# ...Yulun's total backgrounds. 30% flat systematic applied, and 10% MC stat uncertainty applied. dim8 files copied directly from v4 so I don't see errors.
}

# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB'] # 2L_SS v2
# WC_ALL = ['cW', 'cHDD', 'cHW', 'cHWB', 'cHB'] # 2L_SS v3 -- first batch
# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd'] # full set of dim-6
WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0'] # full set of dim-6, a few representative dim-8

L_2018 = 59.83 # fb^-1
L_Run2 = 137.64 # fb^-1
scale_2018_to_Run2 = L_Run2 / L_2018
