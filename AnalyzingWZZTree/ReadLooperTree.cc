#include "Math/LorentzVector.h"
#include "Math/GenVector/LorentzVector.h"
#include "TH1D.h"
#include "TROOT.h"
#include "TFile.h"
#include "TChain.h"

int ReadLooperTree(std::string infile, std::string treeStr)
{
  std::string inputfilename=(infile+".root").c_str();
  TFile *inputFile = new TFile((inputfilename).c_str());
  TChain *tree=new TChain(treeStr.c_str());
  tree->Add(inputfilename.c_str());

  vector<float>   *LHEWeightmgreweighting;
  Float_t         M5l;
  Float_t         PtOnez;
  Float_t         PtTwoz;
  Float_t         Ptzz;  
  Float_t         LHEWeightSM;
  Float_t         LHEWeightFT1;
  Float_t         LHEWeightFT2;
  Float_t         LHEWeightFT3;
  Float_t         LHEWeightFT4;
  Float_t         LHEWeightFT5;
  Float_t         LHEWeightFT6;

  LHEWeightmgreweighting = 0;
  M5l = 0;
  PtOnez = 0;
  PtTwoz = 0;
  Ptzz = 0;
  LHEWeightSM = 0;
  LHEWeightFT1 = 0;
  LHEWeightFT2 = 0;
  LHEWeightFT3 = 0;
  LHEWeightFT4 = 0; 
  LHEWeightFT5 = 0; 
  LHEWeightFT6 = 0; 

  tree->SetBranchAddress("Common_LHEWeight_mg_reweighting", &(LHEWeightmgreweighting));
  tree->SetBranchAddress("M5l", &(M5l));
  tree->SetBranchAddress("PtOnez", &(PtOnez));
  tree->SetBranchAddress("PtTwoz", &(PtTwoz));
  tree->SetBranchAddress("Ptzz", &(Ptzz));
  tree->SetBranchAddress("LHEWeightSM", &(LHEWeightSM));
  tree->SetBranchAddress("LHEWeightFT1", &(LHEWeightFT1));
  tree->SetBranchAddress("LHEWeightFT2", &(LHEWeightFT2));
  tree->SetBranchAddress("LHEWeightFT3", &(LHEWeightFT3));
  tree->SetBranchAddress("LHEWeightFT4", &(LHEWeightFT4));
  tree->SetBranchAddress("LHEWeightFT5", &(LHEWeightFT5));
  tree->SetBranchAddress("LHEWeightFT6", &(LHEWeightFT6));

  TH1D *h_M5l_SM = new TH1D("h_M5l_SM", "h_M5l_SM", 5000, 0.0, 5000.0); h_M5l_SM->Sumw2();
  TH1D *h_M5l_FT0_m100 = new TH1D("h_M5l_FT0_m100", "h_M5l_FT0_m100", 5000, 0.0, 5000.0); h_M5l_FT0_m100->Sumw2();
  TH1D *h_M5l_FT0_m50 = new TH1D("h_M5l_FT0_m50", "h_M5l_FT0_m50", 5000, 0.0, 5000.0); h_M5l_FT0_m50->Sumw2();
  TH1D *h_M5l_FT0_m10 = new TH1D("h_M5l_FT0_m10", "h_M5l_FT0_m10", 5000, 0.0, 5000.0); h_M5l_FT0_m10->Sumw2();
  TH1D *h_M5l_FT0_p10 = new TH1D("h_M5l_FT0_p10", "h_M5l_FT0_p10", 5000, 0.0, 5000.0); h_M5l_FT0_p10->Sumw2();
  TH1D *h_M5l_FT0_p50 = new TH1D("h_M5l_FT0_p50", "h_M5l_FT0_p50", 5000, 0.0, 5000.0); h_M5l_FT0_p50->Sumw2();
  TH1D *h_M5l_FT0_p100 = new TH1D("h_M5l_FT0_p100", "h_M5l_FT0_p100", 5000, 0.0, 5000.0); h_M5l_FT0_p100->Sumw2();

  TH1D *h_Ptzz_SM = new TH1D("h_Ptzz_SM", "h_Ptzz_SM", 5000, 0.0, 5000.0); h_Ptzz_SM->Sumw2();
  TH1D *h_Ptzz_FT0_m100 = new TH1D("h_Ptzz_FT0_m100", "h_Ptzz_FT0_m100", 5000, 0.0, 5000.0); h_Ptzz_FT0_m100->Sumw2();
  TH1D *h_Ptzz_FT0_m50 = new TH1D("h_Ptzz_FT0_m50", "h_Ptzz_FT0_m50", 5000, 0.0, 5000.0); h_Ptzz_FT0_m50->Sumw2();
  TH1D *h_Ptzz_FT0_m10 = new TH1D("h_Ptzz_FT0_m10", "h_Ptzz_FT0_m10", 5000, 0.0, 5000.0); h_Ptzz_FT0_m10->Sumw2();
  TH1D *h_Ptzz_FT0_p10 = new TH1D("h_Ptzz_FT0_p10", "h_Ptzz_FT0_p10", 5000, 0.0, 5000.0); h_Ptzz_FT0_p10->Sumw2();
  TH1D *h_Ptzz_FT0_p50 = new TH1D("h_Ptzz_FT0_p50", "h_Ptzz_FT0_p50", 5000, 0.0, 5000.0); h_Ptzz_FT0_p50->Sumw2();
  TH1D *h_Ptzz_FT0_p100 = new TH1D("h_Ptzz_FT0_p100", "h_Ptzz_FT0_p100", 5000, 0.0, 5000.0); h_Ptzz_FT0_p100->Sumw2();

  int nEvents=tree->GetEntries();
  std::cout << "Reading events = " << nEvents << std::endl;

  for (int i=0; i<nEvents; ++i)
  {
    tree->GetEvent(i);  
    //float weightSM = LHEWeightSM;
    float weightSM = LHEWeightmgreweighting->at(0);
    float weightFT0_m100 = LHEWeightmgreweighting->at(1);
    float weightFT0_m50 = LHEWeightmgreweighting->at(2);    
    float weightFT0_m10 = LHEWeightmgreweighting->at(3); 
    float weightFT0_p10 = LHEWeightmgreweighting->at(4); 
    float weightFT0_p50 = LHEWeightmgreweighting->at(5); 
    float weightFT0_p100 = LHEWeightmgreweighting->at(6); 

    /*float weightFT8_m100 = LHEWeightmgreweighting->at(7);
    float weightFT8_m50 = LHEWeightmgreweighting->at(8);
    float weightFT8_m10 = LHEWeightmgreweighting->at(9);
    float weightFT8_p10 = LHEWeightmgreweighting->at(10);
    float weightFT8_p50 = LHEWeightmgreweighting->at(11);
    float weightFT8_p100 = LHEWeightmgreweighting->at(12);

    float weightFT9_m100 = LHEWeightmgreweighting->at(13);
    float weightFT9_m50 = LHEWeightmgreweighting->at(14);
    float weightFT9_m10 = LHEWeightmgreweighting->at(15);
    float weightFT9_p10 = LHEWeightmgreweighting->at(16);
    float weightFT9_p50 = LHEWeightmgreweighting->at(17);
    float weightFT9_p100 = LHEWeightmgreweighting->at(18);

    float weightFT0_m100 = LHEWeightFT1;
    float weightFT0_m50 = LHEWeightFT2;
    float weightFT0_m10 = LHEWeightFT3;
    float weightFT0_p10 = LHEWeightFT4;
    float weightFT0_p50 = LHEWeightFT5;
    float weightFT0_p100 = LHEWeightFT6;
    */

    if(weightSM==0) continue;

    h_M5l_SM->Fill(M5l, weightSM);
    h_M5l_FT0_m100->Fill(M5l, weightFT0_m100);
    h_M5l_FT0_m50->Fill(M5l, weightFT0_m50);
    h_M5l_FT0_m10->Fill(M5l, weightFT0_m10);
    h_M5l_FT0_p10->Fill(M5l, weightFT0_p10);
    h_M5l_FT0_p50->Fill(M5l, weightFT0_p50);
    h_M5l_FT0_p100->Fill(M5l, weightFT0_p100);
    
    h_Ptzz_SM->Fill(Ptzz, weightSM);
    h_Ptzz_FT0_m100->Fill(Ptzz, weightFT0_m100);
    h_Ptzz_FT0_m50->Fill(Ptzz, weightFT0_m50);
    h_Ptzz_FT0_m10->Fill(Ptzz, weightFT0_m10);
    h_Ptzz_FT0_p10->Fill(Ptzz, weightFT0_p10);
    h_Ptzz_FT0_p50->Fill(Ptzz, weightFT0_p50);
    h_Ptzz_FT0_p100->Fill(Ptzz, weightFT0_p100);
  } 

  std::string histfilename=("output_"+infile+".root").c_str();
  TFile *tFile=new TFile(histfilename.c_str(), "RECREATE");
  h_M5l_SM->Write();
  h_M5l_FT0_m100->Write();
  h_M5l_FT0_m50->Write();
  h_M5l_FT0_m10->Write();
  h_M5l_FT0_p10->Write();
  h_M5l_FT0_p50->Write();
  h_M5l_FT0_p100->Write();
  h_Ptzz_SM->Write();
  h_Ptzz_FT0_m100->Write();
  h_Ptzz_FT0_m50->Write();
  h_Ptzz_FT0_m10->Write();
  h_Ptzz_FT0_p10->Write();
  h_Ptzz_FT0_p50->Write();
  h_Ptzz_FT0_p100->Write();  

  tFile->Close();
  inputFile->Close();
  std::cout<<"Wrote output file "<<histfilename<<std::endl;

  return 0;
}
  
