#include "Begin_5Lep.h"

int lep_5Lep_Z1_idx1 = -999;
int lep_5Lep_Z1_idx2 = -999;
int lep_5Lep_Z2_idx1 = -999;
int lep_5Lep_Z2_idx2 = -999;
int lep_5Lep_W_idx = -999;

void select5LepLeptons()
{
    int z_lep1;
    int z_lep2;
    int z_lep3;
    int z_lep4;
    int w_lep;
    z_lep1=z_lep2=z_lep3=z_lep4=w_lep=-999;
    double Mz = 91.1876;
    double pair1massDiff, pair2massDiff;
    pair1massDiff=pair2massDiff=0.0;
    double compare1 = 15;
    double compare2 = 15;

    vector<int>	pdgid=	ana.tx.getBranchLazy<vector<int>	>("Common_lep_pdgid");
    
    for(unsigned int i=0; i<pdgid.size(); i++)
    {
        //std::cout << "pdgid.at(i) = " << pdgid.size() << std::endl;
        for(unsigned int j=0; j<pdgid.size(); j++)
        {
            if(i!=j)//make sure not checking same lepton
            {
                if((pdgid.at(i)*pdgid.at(j))==-121 or (pdgid.at(i)*pdgid.at(j))==-169) //check opposite sign pair
                {
                    pair1massDiff = ((ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[i]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[j]).M() -  Mz);
                    for(unsigned int k=0; k<pdgid.size(); k++)
                    {
                        for(unsigned int l=0; l<pdgid.size(); l++)
                        {
                            if(j!=l and j!=k and i!=k and i!=l)//make sure not checking same lepton
                            {
                                if((pdgid.at(k)*pdgid.at(l))==-121 or (pdgid.at(k)*pdgid.at(l))==-169)
                                {
                                    pair2massDiff = ((ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[k]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[l]).M() -  Mz);
                                    if(fabs(pair1massDiff) < compare1 and fabs(pair2massDiff) < compare2)
                                    {
                                        compare1 = fabs(pair1massDiff);
                                        compare2 = fabs(pair2massDiff);
                                        z_lep1=i;
                                        z_lep2=j;
                                        z_lep3=k;
                                        z_lep4=l;

                                        for(unsigned int m=0; m<pdgid.size(); m++)
                                        {
                                          if(i!=m and j!=m and k!=m and l!=m)//make sure not checking same lepton
                                          {
                                             //mT = sqrt(2*ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt()*ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[m].Pt()*(1.0 - cos(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[m].Phi() - ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").phi())));
                                             w_lep=m;
                                          }//w-tag
                                        }//m-loop
                                     }//zz-tag
                                  }//second opposite sign pair
                               }//lepton index check
                            }//l-loop
                         }//k-loop
                      }//first opposite sign pair
                    }//lepton index check
                 }//j-loop
              }//i-loop

    lep_5Lep_Z1_idx1 = z_lep1;
    lep_5Lep_Z1_idx2 = z_lep2;
    lep_5Lep_Z2_idx1 = z_lep3;
    lep_5Lep_Z2_idx2 = z_lep4;
    lep_5Lep_W_idx = w_lep;
    //if(lep_5Lep_W_idx>0 and lep_5Lep_Z1_idx1>0 and lep_5Lep_Z1_idx2>0 and lep_5Lep_Z2_idx1>0 and lep_5Lep_Z2_idx2>0) std::cout << lep_5Lep_W_idx << std::endl;

    return;
}


void Begin_5Lep()
{
    //==============================================
    // Begin_5Lep:
    // This function gets called prior to the event looping.
    // This is where one declares variables, histograms, event selections for the category 5Lep.
    //==============================================

    // Create variables used in this category.
    // Please follow the convention of <category>_<varname> structure.
    /*ana.tx.createBranch<int>("5Lep_intVar1");
    ana.tx.createBranch<float>("5Lep_floatVar1");
    ana.tx.createBranch<LorentzVector>("5Lep_LVVar1");

    // Define selections
    // CommonCut will contain selections that should be common to all categories, starting from this cut, add cuts for this category of the analysis.
    ana.cutflow.getCut("CommonCut");
    ana.cutflow.addCutToLastActiveCut("Cut_5Lep_Preselection", [&]() { return ana.tx.getBranch<LorentzVector>("5Lep_LVVar1").pt() > 25.;}, [&]() { return ana.tx.getBranch<float>("5Lep_floatVar1"); } );

    // Create histograms used in this category.
    // Please follow the convention of h_<category>_<varname> structure.
    // N.B. Using nbins of size 180 or 360 can provide flexibility as it can be rebinned easily, as 180, 360 are highly composite numbers.
    RooUtil::Histograms hists_5Lep;
    hists_5Lep.addHistogram("h_5Lep_intVar1", 10, 0, 10, [&]() { return ana.tx.getBranch<int>("5Lep_intVar1"); } );
    hists_5Lep.addHistogram("h_5Lep_floatVar1", 180, 0, 500, [&]() { return ana.tx.getBranch<float>("5Lep_floatVar1"); } );
    hists_5Lep.addHistogram("h_5Lep_LVVar1_Pt", 180, 0, 150, [&]() { return ana.tx.getBranch<LorentzVector>("5Lep_LVVar1").pt(); } );

    // Now book cutflow histogram (could be commented out if user does not want.)
    // N.B. Cutflow histogramming can be CPU consuming.
    ana.cutflow.bookCutflows();

    // Book histograms to cuts that user wants for this category.
    ana.cutflow.bookHistogramsForCut(hists_5Lep, "Cut_5Lep_Preselection");*/
    ana.tx.createBranch<float>("5Lep_lep1_pt"               );
    ana.tx.createBranch<float>("5Lep_lep2_pt"               );
    ana.tx.createBranch<float>("5Lep_lep3_pt"               );
    ana.tx.createBranch<float>("5Lep_lep4_pt"               );
    ana.tx.createBranch<float>("5Lep_lep5_pt"               );
    ana.tx.createBranch<float>("5Lep_lep1_eta"               );
    ana.tx.createBranch<float>("5Lep_lep2_eta"               );
    ana.tx.createBranch<float>("5Lep_lep3_eta"               );
    ana.tx.createBranch<float>("5Lep_lep4_eta"               );
    ana.tx.createBranch<float>("5Lep_lep5_eta"               );
    ana.tx.createBranch<float>("5Lep_lep1_phi"               );
    ana.tx.createBranch<float>("5Lep_lep2_phi"               );
    ana.tx.createBranch<float>("5Lep_lep3_phi"               );
    ana.tx.createBranch<float>("5Lep_lep4_phi"               );
    ana.tx.createBranch<float>("5Lep_lep5_phi"               );
    ana.tx.createBranch<float>("5Lep_lep1_energy"               );
    ana.tx.createBranch<float>("5Lep_lep2_energy"               );
    ana.tx.createBranch<float>("5Lep_lep3_energy"               );
    ana.tx.createBranch<float>("5Lep_lep4_energy"               );
    ana.tx.createBranch<float>("5Lep_lep5_energy"               );
    ana.tx.createBranch<int>("5Lep_lep1_pdgid"               );
    ana.tx.createBranch<int>("5Lep_lep2_pdgid"               );
    ana.tx.createBranch<int>("5Lep_lep3_pdgid"               );
    ana.tx.createBranch<int>("5Lep_lep4_pdgid"               );
    ana.tx.createBranch<int>("5Lep_lep5_pdgid"               );
    ana.tx.createBranch<float>("5Lep_MET"                   );
    ana.tx.createBranch<float>("5Lep_genMVVV"               );
    ana.tx.createBranch<float>("5Lep_genpTVVV"              );
    ana.tx.createBranch<float>("5Lep_LHEWeightSM"           );
    ana.tx.createBranch<float>("5Lep_LHEWeightDefault"      );
    ana.tx.createBranch<float>("5Lep_nJet"                  );
    ana.tx.createBranch<int>("5Lep_nb_medium"               );
    ana.tx.createBranch<float>("5Lep_Zcand1"                   );
    ana.tx.createBranch<float>("5Lep_Zcand2"                   );
    ana.tx.createBranch<float>("5Lep_Wcand"                   );
    ana.tx.createBranch<float>("5Lep_Zcand1_SR"                   );
    ana.tx.createBranch<float>("5Lep_Zcand2_SR"                   );
    ana.tx.createBranch<float>("5Lep_Wcand_SR"                   );
    // Define selections
    // CommonCut will contain selections that should be common to all categories, starting from this cut, add cuts for this category of the analysis.
    ana.cutflow.getCut("CommonCut");
    ana.cutflow.addCutToLastActiveCut("Cut_5Lep_AllLeps",
                                      [&]()
                                      {
                                         //6 leptons
                                        if ((ana.tx.getBranchLazy<vector<int> >("Common_lep_pdgid").size() == 5)) return true;
                                        else return false;
                                      //}, [&]() { return ana.tx.getBranchLazy<float>("Common_event_lepSF"); });
                                       }, UNITY );
    ana.cutflow.addCutToLastActiveCut("Cut_5Lep_Trigger",
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
    ana.cutflow.addCutToLastActiveCut("Cut_5Lep_Preselection",
    				      [&]()
                                      {
                                        //make some default setting - overwrite later
                                        ana.tx.setBranch<float>("5Lep_lep1_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].Pt());
                                        ana.tx.setBranch<float>("5Lep_lep2_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].Pt());
                                        ana.tx.setBranch<float>("5Lep_lep3_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].Pt());
                                        ana.tx.setBranch<float>("5Lep_lep4_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].Pt());
                                        ana.tx.setBranch<float>("5Lep_lep5_pt",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].Pt());
 					ana.tx.setBranch<float>("5Lep_lep1_eta",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].Eta());
                                        ana.tx.setBranch<float>("5Lep_lep2_eta",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].Eta());
                                        ana.tx.setBranch<float>("5Lep_lep3_eta",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].Eta());
                                        ana.tx.setBranch<float>("5Lep_lep4_eta",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].Eta());
                                        ana.tx.setBranch<float>("5Lep_lep5_eta",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].Eta());
                                        ana.tx.setBranch<float>("5Lep_lep1_phi",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].Phi());
                                        ana.tx.setBranch<float>("5Lep_lep2_phi",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].Phi());
                                        ana.tx.setBranch<float>("5Lep_lep3_phi",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].Phi());
                                        ana.tx.setBranch<float>("5Lep_lep4_phi",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].Phi());
                                        ana.tx.setBranch<float>("5Lep_lep5_phi",               ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].Phi());   
                                        ana.tx.setBranch<float>("5Lep_lep1_energy",              ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[0].E());
                                        ana.tx.setBranch<float>("5Lep_lep2_energy",              ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[1].E());
                                        ana.tx.setBranch<float>("5Lep_lep3_energy",              ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[2].E());
                                        ana.tx.setBranch<float>("5Lep_lep4_energy",              ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[3].E());
                                        ana.tx.setBranch<float>("5Lep_lep5_energy",              ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[4].E());
                                        ana.tx.setBranch<int>("5Lep_lep1_pdgid",               ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[0]);
 					ana.tx.setBranch<int>("5Lep_lep2_pdgid",               ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[1]);
                                        ana.tx.setBranch<int>("5Lep_lep3_pdgid",               ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[2]);
                                        ana.tx.setBranch<int>("5Lep_lep4_pdgid",               ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[3]);
                                        ana.tx.setBranch<int>("5Lep_lep5_pdgid",               ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[4]);          
                                        ana.tx.setBranch<float>("5Lep_genMVVV",               -999.);
                                        ana.tx.setBranch<float>("5Lep_MET",                   ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt());
                                        ana.tx.setBranch<float>("5Lep_nJet",                  ana.tx.getBranchLazy<vector<int>>("Common_jet_idxs").size());
                                        ana.tx.setBranch<int>("5Lep_nb_medium",               ana.tx.getBranchLazy<int>("Common_nb_medium"));
                                        //ana.tx.setBranch<float>("5Lep_LHEWeightSM",           nt.LHEWeight_mg_reweighting()[0]);
                                        select5LepLeptons();

 					if(lep_5Lep_Z1_idx1 >= 0 and lep_5Lep_Z1_idx2 >= 0 and lep_5Lep_Z2_idx1 >= 0 and lep_5Lep_Z2_idx2 >= 0 and lep_5Lep_W_idx >= 0)
                                        {
                                          if(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx1].Pt() > 25.0 and ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx2].Pt() > 10.0 and ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx1].Pt() > 25.0 and ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx1].Pt() > 10.0)
                                          { 
                                            ana.tx.setBranch<float>("5Lep_Zcand1",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx2]).M());
                                            ana.tx.setBranch<float>("5Lep_Zcand2",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx2]).M());
                                            ana.tx.setBranch<float>("5Lep_Wcand",                    (sqrt(2*ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt()*ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Pt()*(1.0 - cos(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Phi() - ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").phi())))));              
                                            if(abs(ana.tx.getBranchLazy<vector<int>>("Common_lep_pdgid")[lep_5Lep_W_idx])==11)
                                            {
                                              double mT = sqrt(2*ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt()*ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Pt()*(1.0 - cos(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Phi() - ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").phi())));
                                              if(mT > 50.0)
                                              {
                                                ana.tx.setBranch<float>("5Lep_Zcand1_SR",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx2]).M());
                                                ana.tx.setBranch<float>("5Lep_Zcand2_SR",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx2]).M());
                                                ana.tx.setBranch<float>("5Lep_Wcand_SR",                    (sqrt(2*ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt()*ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Pt()*(1.0 - cos(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Phi() - ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").phi())))));
                                              }  
                                            }
                                            else
                                            {
                                              ana.tx.setBranch<float>("5Lep_Zcand1_SR",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z1_idx2]).M());
                                              ana.tx.setBranch<float>("5Lep_Zcand2_SR",                   (ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx1]+ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_Z2_idx2]).M());
                                              ana.tx.setBranch<float>("5Lep_Wcand_SR",                    (sqrt(2*ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").pt()*ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Pt()*(1.0 - cos(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_lep_p4")[lep_5Lep_W_idx].Phi() - ana.tx.getBranchLazy<LorentzVector>("Common_met_p4").phi())))));
                                            }
                                          }
                                        }
                                        if(ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s").size()==5){
                                          LorentzVector genVVV = LorentzVector(0.,0.,0.,0.);
                                          for(unsigned int gi = 0; gi < ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s").size(); ++gi){
                                            genVVV +=  ana.tx.getBranchLazy<vector<LorentzVector>>("Common_gen_vvvdecay_p4s")[gi];
                                          }
                                          ana.tx.setBranch<float>("5Lep_genMVVV",  genVVV.M() );
                                          ana.tx.setBranch<float>("5Lep_genpTVVV", genVVV.Pt());
                                        }
                                        return true;
                                      }, UNITY);// trigger SF would go in here instead of UNITY, in principle also btag weight
    // --------------------
    // ***      OF      ***
    // --------------------
    ana.cutflow.getCut("Cut_5Lep_Preselection");
    ana.histograms.addHistogram("genVVV_M"     , 450,   0,  4500, [&]() { return      ana.tx.getBranch<float>("5Lep_genMVVV"                 )   ; } );
    //ana.histograms.addHistogram("LHESMWeight"  , 2000,   0,  2.0, [&]() { return      ana.tx.getBranch<float>("5Lep_LHEWeightSM"             )   ; } );
    //ana.histograms.addHistogram("LogLHESMWeight", 300, -29.,  1.0, [&]() { return  log(ana.tx.getBranch<float>("5Lep_LHEWeightSM")    )   ; } );
    //ana.histograms.addHistogram("LHESMWeight_lowMET"  ,  2200,-0.1,  2.1, [&]() { return   ana.tx.getBranch<float>("5Lep_MET") < 400. ? ana.tx.getBranch<float>("5Lep_LHEWeightSM") : -999.   ; } );
    RooUtil::Histograms hists_5Lep;

    // Now book cutflow histogram (could be commented out if user does not want.)
    // N.B. Cutflow histogramming can be CPU consuming.
    ana.cutflow.bookCutflows();

    // Book histograms to cuts that user wants for this category.
    ana.cutflow.bookHistogramsForCutAndBelow(ana.histograms, "Cut_5Lep_Preselection"); 
}
