# store version of each channel to use when running combine
# also track what integrated luminosity is in that version of the yield file
dim6_WCs = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd'] # full set of dim-6
dim8_WCs = ['FS0', 'FS1', 'FS2', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4', 'FM5', 'FM7', 'FT0', 'FT1', 'FT2', 'FT3', 'FT4', 'FT5', 'FT6', 'FT7', 'FT8', 'FT9'] # full set of dim-8
# sorting like SMP-10-012 (FT, FM, FS)
dim8_WCs_sort_AN = ['FT0', 'FT1', 'FT2', 'FT3', 'FT4', 'FT5', 'FT6', 'FT7', 'FT8', 'FT9', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4', 'FM5', 'FM7', 'FS0', 'FS1', 'FS2'] # full set of dim-8
#dim8_WCs_1T = ['FS0', 'FS1', 'FS2', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4', 'FM5', 'FM7', 'FT0', 'FT1', 'FT2', 'FT3', 'FT4', 'FT5', 'FT6', 'FT7', 'FT8'] # FT9 missing
dim8_WCs_1T = dim8_WCs
WCs_clip_dim6 = dim6_WCs # all
WCs_clip_dim8 = dim8_WCs # all
#WCs_clip = ['FT0'] # dev
# 2 dim8 for debug
#dim8_WCs = ['FT0', 'FM0']
versions_dict = {
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_2FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHDD', 'cHW', 'cHB', 'cHWB']}, # no systematics
    # '0Lepton_2FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not suppressed.
    # '0Lepton_2FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_2FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_2FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updates.
    # '0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    #'0Lepton_2FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    #'0Lepton_2FJ': {'v': 18, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 1D complete, with all systematics. Missing VH.
    #'0Lepton_2FJ': {'v': 20, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # wtag sf added; VH fixed; JES fixed.
    #'0Lepton_2FJ': {'v': 21, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # alternate binning test (3 bins)
    #'0Lepton_2FJ': {'v': 23, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # most uncertainties fixed
    # '0Lepton_2FJ': {'v': 24, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # dim8 added
    '0Lepton_2FJ': {'v': 24, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
                    'v_NDIM': 25, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, #  dim8 added, NDIM added
    # '0Lepton_3FJ': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points'},
    # '0Lepton_3FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points'}, # rebinning test, no systematics, more 1D scans
    # '0Lepton_3FJ': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW']}, # no systematics, multi-operators not finished yet
    # '0Lepton_3FJ': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points'}, # no systematics, SMHLOOP not supressed.
    # '0Lepton_3FJ': {'v': 12, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # no systematics, update to VVV+1Jet. QCD background update.
    # '0Lepton_3FJ': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ rebinning. VVV yield breakdown
    # '0Lepton_3FJ': {'v': 14, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # 0L_2FJ bg estimate updated. 0L_3FJ minor updatees.
    # '0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0']}, # dim8: FT0 WWW only. Binning changed for 2FJ.
    #'0Lepton_3FJ': {'v': 15, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim8: FT0, FM0 VVV. Binning back to v14 2FJ.
    #'0Lepton_3FJ': {'v': 18, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 1D complete, with all systematics. Missing VH.
    #'0Lepton_3FJ': {'v': 20, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # wtag sf added; VH fixed; JES fixed.
    #'0Lepton_3FJ': {'v': 21, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # alternate binning test (3 bins)
    #'0Lepton_3FJ': {'v': 23, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # most uncertainties fixed
    #'0Lepton_3FJ': {'v': 24, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # dim8 added
    '0Lepton_3FJ': {'v': 24, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
                    'v_NDIM': 25, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, #  dim8 added, NDIM added
    # '1Lepton': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '1Lepton': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # cW -> VVV+1Jet, all other dim6 added. autoMCStats should be turned off.
    #'1Lepton': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # All dim8 added (dim6 bugged). Processed only FT0, FM0. autoMCStats should be turned off.
    #'1Lepton': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # Signal systematics added for dim6 and dim8 (missing PDF, alpha_s, QCD_scales). All dim8 added. Processed only FT0, FM0. autoMCStats should be turned off.
    #'1Lepton': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics. Items to debug (JES and JER removed due to bugs; Vgamma is missing; trigger_weight_ is missing; SM is using EFT scan values)
    #'1Lepton': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # same as v5, with FJ SF fixed (include Z).
    #'1Lepton': {'v': 1000, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # same as v6, switch to 4 bins.
    #'1Lepton': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # includes pT dependent SFs
    #'1Lepton': {'v': 8, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
    #            'v_NDIM': 8, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # includes dim8, MultiDim (refactored)
    '1Lepton': {'v': 9, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
               'v_NDIM': 8, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # update to central
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
    #'2Lepton_OS': {'v': 13, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics. Items to debug (SM is using EFT scan values; systematics for cHu removed due to bug). Previous items fixed, but now there is a bug in SFs (signal yield increased but should decrease)
    #'2Lepton_OS': {'v': 16, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics. Double count bug fixed. wtag sf to be updated (include Z)
    #'2Lepton_OS': {'v': 17, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # wtag sf updated
    #'2Lepton_OS': {'v': 18, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # signal sf bug fixed, data-driven predictions now include wtag sf. DY is much larger than before -- working to understand this.
    #'2Lepton_OS': {'v': 19, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # small change in alpha_s
    #'2Lepton_OS': {'v': 20, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # includes pT dependent SFs; bkg uncertainties no longer flat
    #'2Lepton_OS': {'v': 20, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # includes pT dependent SFs; bkg uncertainties no longer flat; dim8 WCs added 10-10-24
    #'2Lepton_OS': {'v': 20, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
    #               'v_NDIM': 20, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # includes pT dependent SFs; bkg uncertainties no longer flat; dim8 WCs added 10-10-24; MultiDim (refactored)
    #'2Lepton_OS': {'v': 21, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
    #              'v_NDIM': 20, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # dim6 central; dim8 copied from v20
    '2Lepton_OS': {'v': 22, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
                   'v_NDIM': 20, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # syst bug fix dim6 central; dim8 copied from v20
    #'2Lepton_OS_2FJ': {'v': 2, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete / first official pass, with all systematics.
    #'2Lepton_OS_2FJ': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete. everything in place except wtag sf
    #'2Lepton_OS_2FJ': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # wtag sf added. switched from 2018 scaled to Run2 lumi to using all 3 years.
    #'2Lepton_OS_2FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # includes pT dependent SFs; background uncertainties updated; dim8 WCs added 10-10-24
    '2Lepton_OS_2FJ': {'v': 6, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
                       'v_NDIM': 6, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, #  includes pT dependent SFs; background uncertainties updated; dim8 WCs added 10-10-24; MultiDim (refactored)
    # '2Lepton_SS': {'v': 1, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']},
    # '2Lepton_SS': {'v': 2, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1']}, # only WWW
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW']}, # VVV, but only cW -- first batch
    # '2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # VVV 1J
    #'2Lepton_SS': {'v': 3, 'lumi': '2018', 'EFT_type': 'params', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # VVV 1J, same as previous line with dim8 added.
    #'2Lepton_SS': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # dim6 signal systematics added with a few missing (PDF, alpha_s, QCD_scales). TTbar updated to data driven (including uncertainty). dim8 missing but added by hand from cleaned v3 file.
    #'2Lepton_SS': {'v': 5, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # updated systematics. binning has changed and dim8 still not ready, so removed it from 2L_SS operators. Be aware of this when looking at the results before this is added in again.
    #'2Lepton_SS': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # dim6 complete, with all systematics.
    #'2Lepton_SS': {'v': 8, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # same as v7 .
    #'2Lepton_SS': {'v': 9, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # includes pT dependent SFs
    # '2Lepton_SS': {'v': 10, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # multidim, no signal systematics
    #'2Lepton_SS': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # multidim, with signal systematics
    #'2Lepton_SS': {'v': 9, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
    #               'v_NDIM': 9, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # includes pT dependent SFs, dim8, MultiDim (refactored)
    '2Lepton_SS': {'v': 11, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs,
                  'v_NDIM': 9, 'EFT_ops_NDIM': dim6_WCs, 'unblind': False}, # update to central
    # '2Lepton_SS': {'v': 1001, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # TEST!! of Yulun's proposal for EFTfitCoefficient matrix for analysts to report yields. This is supplied for dim6 at the inclusive level of the analysis with dilepton filter. I have rebinned the matrix for sT to look like Yulun's SR binning. I added a single background that roughly corresponds to...
    #'2Lepton_SS': {'v': 1002, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0']}, # TEST!! of Yulun's proposal for EFTfitCoefficient matrix for analysts to report yields. This is supplied for dim6 in the signal region. I added a single background that corresponds to...
    # ...Yulun's total backgrounds. 30% flat systematic applied, and 10% MC stat uncertainty applied. dim8 files copied directly from v4 so I don't see errors.
    # TAU TESTS
    #'0Lepton_1T': {'v': 0, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']},
    #'0Lepton_1T': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']}, # updated uncertainties (bkg summed in quadrature; more signal systematics) -- removed after v1.
    #'1Lepton_1T': {'v': 0, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']},
    #'1Lepton_1T': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # updated uncertainties (bkg summed in quadrature; more signal systematics)
    #'1Lepton_1T': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T}, # dim8 added
    #'1Lepton_1T': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #               'v_NDIM': 7, 'EFT_ops_NDIM': dim6_WCs}, # added NDIM (to update 1D)
    # '1Lepton_1T': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 7, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # added NDIM; 1D signal fix
    # '1Lepton_1T': {'v': 17, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 17, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis
    # '1Lepton_1T': {'v': 19, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 19, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis
    '1Lepton_1T': {'v': 26, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
                   'v_NDIM': 26, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis
    #'1Lepton_1T': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # dim8 bug fix; adding multi-WC inputs
    #'2Lepton_1T': {'v': 0, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd']},
    #'2Lepton_1T': {'v': 1, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs}, # updated uncertainties (bkg summed in quadrature; more signal systematics)
    #'2Lepton_1T': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T}, # dim8 added
    #'2Lepton_1T': {'v': 3, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    # '2Lepton_1T': {'v': 7, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 7, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # added NDIM; 1D signal fix
    # '2Lepton_1T': {'v': 17, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 17, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis
    # '2Lepton_1T': {'v': 19, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
    #                'v_NDIM': 19, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis
    '2Lepton_1T': {'v': 26, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs_1T,
                   'v_NDIM': 26, 'EFT_ops_NDIM': dim6_WCs, 'unblind': True}, # unblinding for Joseph's thesis

    #'2Lepton_1T': {'v': 4, 'lumi': 'Run2', 'EFT_type': 'points', 'EFT_ops': dim6_WCs+dim8_WCs}, # dim8 bug fix; adding multi-WC inputs
}

# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB'] # 2L_SS v2
# WC_ALL = ['cW', 'cHDD', 'cHW', 'cHWB', 'cHB'] # 2L_SS v3 -- first batch
#WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd'] # full set of dim-6
# WC_ALL = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd', 'cT0', 'cM0'] # full set of dim-6, a few representative dim-8
#####
#dim6_WCs = ['cW', 'cHbox', 'cHDD', 'cHl3', 'cHq1', 'cHq3', 'cHW', 'cHWB', 'cll1', 'cHB', 'cHu', 'cHd'] # full set of dim-6
#dim8_WCs = ['FS0', 'FS1', 'FS2', 'FM0', 'FM1', 'FM2', 'FM3', 'FM4', 'FM5', 'FM7', 'FT0', 'FT1', 'FT2', 'FT3', 'FT4', 'FT5', 'FT6', 'FT7', 'FT8', 'FT9'] # full set of dim-8
# dim6 only
#WC_ALL = dim6_WCs
# dim6 + dim8
WC_ALL = dim6_WCs + dim8_WCs

L_2018 = 59.83 # fb^-1
L_Run2 = 137.64 # fb^-1
scale_2018_to_Run2 = L_Run2 / L_2018
