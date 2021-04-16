#include "Begin_6Lep.h"

void Begin_6Lep()
{
    //==============================================
    // Begin_6Lep:
    // This function gets called prior to the event looping.
    // This is where one declares variables, histograms, event selections for the category 6l.
    //==============================================

    // Create variables used in this category.
    // Please follow the convention of <category>_<varname> structure.
    ana.tx.createBranch<float>("6l_lep1_pt"               );
    ana.tx.createBranch<float>("6l_lep2_pt"               );
    ana.tx.createBranch<float>("6l_lep3_pt"               );
    ana.tx.createBranch<float>("6l_lep4_pt"               );
    ana.tx.createBranch<float>("6l_lep5_pt"               );
    ana.tx.createBranch<float>("6l_lep6_pt"               );
    ana.tx.createBranch<float>("6l_MET"                   );
    ana.tx.createBranch<float>("6l_ST"                    );
    ana.tx.createBranch<float>("6l_genMVVV"               );
    ana.tx.createBranch<float>("6l_LHEWeightSM"           );
    ana.tx.createBranch<float>("6l_LHEWeightDefault"      );
    ana.tx.createBranch<float>("6l_nJet"                  );
    // Define selections
    // CommonCut will contain selections that should be common to all categories, starting from this cut, add cuts for this category of the analysis.
    ana.cutflow.getCut("CommonCut");
    ana.cutflow.addCutToLastActiveCut("Cut_6Lep_AllLeps",
                                      [&]()
                                      {
                                         //6 leptons
                                        if ((ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid").size() >= 6)) return true;
                                        else return false;
                                      //}, [&]() { return ana.tx.getBranchLazy<float>("Common_event_lepSF"); });
                                       }, UNITY );
    ana.cutflow.addCutToLastActiveCut("Cut_6Lep_Trigger",
                                      [&]()
                                      {
                                        // test trigger bits
                                        //if (nt.isData()){// run only on data
                                        if (true){// run on data and simulation
                                          if(nt.isData() && !(ana.tx.getBranchLazy<bool>("Common_pass_duplicate_removal_mm_em_ee"))) return false;
                                          if(abs(ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[0]*ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[1])==121){
                                            if(!ana.tx.getBranchLazy<bool>("Common_HLT_DoubleEl")) return false;
                                          }
                                          if(abs(ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[0]*ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[1])==169){
                                            if(!ana.tx.getBranchLazy<bool>("Common_HLT_DoubleMu")) return false;
                                          }
                                          if(abs(ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[0]*ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid")[1])==143){
                                            if(!ana.tx.getBranchLazy<bool>("Common_HLT_MuEG")) return false;
                                          }
                                        }
                                        return true;
                                      }, UNITY);
    ana.cutflow.addCutToLastActiveCut("Cut_6Lep_Preselection",
                                      [&]()
                                      {
                                        //make some default setting - overwrite later
                                        ana.tx.setBranch<float>("6l_lep1_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].Pt());
                                        ana.tx.setBranch<float>("6l_lep2_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].Pt());
                                        ana.tx.setBranch<float>("6l_lep3_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].Pt());
                                        ana.tx.setBranch<float>("6l_lep4_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].Pt());
                                        ana.tx.setBranch<float>("6l_lep5_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].Pt());
                                        ana.tx.setBranch<float>("6l_lep6_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[5].Pt());
                                        ana.tx.setBranch<float>("6l_genMVVV",               -999.);
                                        ana.tx.setBranch<float>("6l_MET",                   ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt());
                                        ana.tx.setBranch<float>("6l_nJet",                  ana.tx.getBranchLazy<vector<int>>("Common_jet_idxs").size());
                                        ana.tx.setBranch<float>("6l_ST",                    (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].Pt() + ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].Pt()+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].Pt()+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].Pt()+ ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].Pt()+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[5].Pt())); 
                                        //ana.tx.setBranch<float>("6l_LHEWeightSM",           nt.LHEWeight_mg_reweighting()[0]);
                                        
                                        if(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s").size()>=6){
                                          LorentzVector genVVV = LorentzVector(0.,0.,0.,0.);
                                          for(unsigned int gi = 0; gi < ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s").size(); ++gi){
                                            genVVV +=  ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s")[gi];
                                          }
                                          ana.tx.setBranch<float>("6l_genMVVV",  genVVV.M() );
                                          //ana.tx.setBranch<float>("6l_genpTVVV", genVVV.Pt());
                                        }
                                        return true;
                                      }, UNITY);// trigger SF would go in here instead of UNITY, in principle also btag weight
    // --------------------
    // ***      OF      ***
    // --------------------
    ana.cutflow.getCut("Cut_6Lep_Preselection");
    ana.histograms.addHistogram("genVVV_M"     , 450,   0,  4500, [&]() { return      ana.tx.getBranch<float>("6l_genMVVV"                 )   ; } );
    ana.histograms.addHistogram("6l_ST"     ,    100,   0,  1000, [&]() { return      ana.tx.getBranch<float>("6l_ST"                 )   ; } ); 
    //ana.histograms.addHistogram("LHESMWeight"  , 2000,   0,  2.0, [&]() { return      ana.tx.getBranch<float>("6l_LHEWeightSM"             )   ; } );
    //ana.histograms.addHistogram("LogLHESMWeight", 300, -29.,  1.0, [&]() { return  log(ana.tx.getBranch<float>("6l_LHEWeightSM")    )   ; } );
    //ana.histograms.addHistogram("LHESMWeight_lowMET"  ,  2200,-0.1,  2.1, [&]() { return   ana.tx.getBranch<float>("6l_MET") < 400. ? ana.tx.getBranch<float>("6l_LHEWeightSM") : -999.   ; } );
    RooUtil::Histograms hists_6Lep;

    // Now book cutflow histogram (could be commented out if user does not want.)
    // N.B. Cutflow histogramming can be CPU consuming.
    ana.cutflow.bookCutflows();

    // Book histograms to cuts that user wants for this category.
    ana.cutflow.bookHistogramsForCutAndBelow(ana.histograms, "Cut_6Lep_Preselection");
}
