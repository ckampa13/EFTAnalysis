#include "Math/LorentzVector.h"
#include "Math/GenVector/LorentzVector.h"
#include "TH1D.h"
#include "TROOT.h"
#include "TFile.h"
#include "TChain.h"

int ReadLooperTree_ZZZ(std::string infile, std::string treeStr)
{
  std::string inputfilename=(infile+".root").c_str();
  TFile *inputFile = new TFile((inputfilename).c_str());
  TChain *tree=new TChain(treeStr.c_str());
  tree->Add(inputfilename.c_str());

  //vector<float>   *LHEWeightmgreweightingtimesgenWeight;
  vector<float>   *LHEWeightmgreweighting;
  Float_t         ST;
  Float_t         m6l;
  Float_t         LHEWeightSM;
  Float_t         LHEWeightFT1;
  Float_t         LHEWeightFT2;
  Float_t         LHEWeightFT3;
  Float_t         LHEWeightFT4;
  Float_t         LHEWeightFT5;
  Float_t         LHEWeightFT6;

  LHEWeightmgreweighting = 0;
  m6l = 0;
  ST = 0;
  LHEWeightSM = 0;
  LHEWeightFT1 = 0;
  LHEWeightFT2 = 0;
  LHEWeightFT3 = 0;
  LHEWeightFT4 = 0; 
  LHEWeightFT5 = 0; 
  LHEWeightFT6 = 0; 
 
  //tree->SetBranchAddress("Root__h_Common_LHEWeight_mg_reweighting_times_genWeight", &(LHEWeightmgreweightingtimesgenWeight));
  tree->SetBranchAddress("Common_LHEWeight_mg_reweighting", &(LHEWeightmgreweighting));
  tree->SetBranchAddress("ST", &(ST));
  tree->SetBranchAddress("m6l", &(m6l));
  tree->SetBranchAddress("LHEWeightSM", &(LHEWeightSM));
  tree->SetBranchAddress("LHEWeightFT1", &(LHEWeightFT1));
  tree->SetBranchAddress("LHEWeightFT2", &(LHEWeightFT2));
  tree->SetBranchAddress("LHEWeightFT3", &(LHEWeightFT3));
  tree->SetBranchAddress("LHEWeightFT4", &(LHEWeightFT4));
  tree->SetBranchAddress("LHEWeightFT5", &(LHEWeightFT5));
  tree->SetBranchAddress("LHEWeightFT6", &(LHEWeightFT6));

  TH1D *h_nEvents_SM = new TH1D("h_nEvents_SM", "h_nEvents_SM", 10, -0.5, 10.5); h_nEvents_SM->Sumw2();
  TH1D *h_nEvents_FT0_m100 = new TH1D("h_nEvents_FT0_m100", "h_nEvents_FT0_m100", 10, -0.5, 10.5); h_nEvents_FT0_m100->Sumw2();
  TH1D *h_nEvents_FT0_m50 = new TH1D("h_nEvents_FT0_m50", "h_nEvents_FT0_m50", 10, -0.5, 10.5); h_nEvents_FT0_m50->Sumw2();
  TH1D *h_nEvents_FT0_m10 = new TH1D("h_nEvents_FT0_m10", "h_nEvents_FT0_m10", 10, -0.5, 10.5); h_nEvents_FT0_m10->Sumw2();
  TH1D *h_nEvents_FT0_p10 = new TH1D("h_nEvents_FT0_p10", "h_nEvents_FT0_p10", 10, -0.5, 10.5); h_nEvents_FT0_p10->Sumw2();
  TH1D *h_nEvents_FT0_p50 = new TH1D("h_nEvents_FT0_p50", "h_nEvents_FT0_p50", 10, -0.5, 10.5); h_nEvents_FT0_p50->Sumw2();
  TH1D *h_nEvents_FT0_p100 = new TH1D("h_nEvents_FT0_p100", "h_nEvents_FT0_p100", 10, -0.5, 10.5); h_nEvents_FT0_p100->Sumw2();

  TH1D *h_nEvents_FT8_m100 = new TH1D("h_nEvents_FT8_m100", "h_nEvents_FT8_m100", 10, -0.5, 10.5); h_nEvents_FT8_m100->Sumw2();
  TH1D *h_nEvents_FT8_m50 = new TH1D("h_nEvents_FT8_m50", "h_nEvents_FT8_m50", 10, -0.5, 10.5); h_nEvents_FT8_m50->Sumw2();
  TH1D *h_nEvents_FT8_m10 = new TH1D("h_nEvents_FT8_m10", "h_nEvents_FT8_m10", 10, -0.5, 10.5); h_nEvents_FT8_m10->Sumw2();
  TH1D *h_nEvents_FT8_p10 = new TH1D("h_nEvents_FT8_p10", "h_nEvents_FT8_p10", 10, -0.5, 10.5); h_nEvents_FT8_p10->Sumw2();
  TH1D *h_nEvents_FT8_p50 = new TH1D("h_nEvents_FT8_p50", "h_nEvents_FT8_p50", 10, -0.5, 10.5); h_nEvents_FT8_p50->Sumw2();
  TH1D *h_nEvents_FT8_p100 = new TH1D("h_nEvents_FT8_p100", "h_nEvents_FT8_p100", 10, -0.5, 10.5); h_nEvents_FT8_p100->Sumw2();

  TH1D *h_nEvents_FT9_m100 = new TH1D("h_nEvents_FT9_m100", "h_nEvents_FT9_m100", 10, -0.5, 10.5); h_nEvents_FT9_m100->Sumw2();
  TH1D *h_nEvents_FT9_m50 = new TH1D("h_nEvents_FT9_m50", "h_nEvents_FT9_m50", 10, -0.5, 10.5); h_nEvents_FT9_m50->Sumw2();
  TH1D *h_nEvents_FT9_m10 = new TH1D("h_nEvents_FT9_m10", "h_nEvents_FT9_m10", 10, -0.5, 10.5); h_nEvents_FT9_m10->Sumw2();
  TH1D *h_nEvents_FT9_p10 = new TH1D("h_nEvents_FT9_p10", "h_nEvents_FT9_p10", 10, -0.5, 10.5); h_nEvents_FT9_p10->Sumw2();
  TH1D *h_nEvents_FT9_p50 = new TH1D("h_nEvents_FT9_p50", "h_nEvents_FT9_p50", 10, -0.5, 10.5); h_nEvents_FT9_p50->Sumw2();
  TH1D *h_nEvents_FT9_p100 = new TH1D("h_nEvents_FT9_p100", "h_nEvents_FT9_p100", 10, -0.5, 10.5); h_nEvents_FT9_p100->Sumw2();

  TH1D *h_m6l_SM = new TH1D("h_m6l_SM", "h_m6l_SM", 5000, 0.0, 5000.0); h_m6l_SM->Sumw2();
  TH1D *h_m6l_FT0_m100 = new TH1D("h_m6l_FT0_m100", "h_m6l_FT0_m100", 5000, 0.0, 5000.0); h_m6l_FT0_m100->Sumw2();
  TH1D *h_m6l_FT0_m50 = new TH1D("h_m6l_FT0_m50", "h_m6l_FT0_m50", 5000, 0.0, 5000.0); h_m6l_FT0_m50->Sumw2();
  TH1D *h_m6l_FT0_m10 = new TH1D("h_m6l_FT0_m10", "h_m6l_FT0_m10", 5000, 0.0, 5000.0); h_m6l_FT0_m10->Sumw2();
  TH1D *h_m6l_FT0_p10 = new TH1D("h_m6l_FT0_p10", "h_m6l_FT0_p10", 5000, 0.0, 5000.0); h_m6l_FT0_p10->Sumw2();
  TH1D *h_m6l_FT0_p50 = new TH1D("h_m6l_FT0_p50", "h_m6l_FT0_p50", 5000, 0.0, 5000.0); h_m6l_FT0_p50->Sumw2();
  TH1D *h_m6l_FT0_p100 = new TH1D("h_m6l_FT0_p100", "h_m6l_FT0_p100", 5000, 0.0, 5000.0); h_m6l_FT0_p100->Sumw2();

  TH1D *h_ST_SM = new TH1D("h_ST_SM", "h_ST_SM", 5000, 0.0, 5000.0); h_ST_SM->Sumw2();
  TH1D *h_ST_FT0_m100 = new TH1D("h_ST_FT0_m100", "h_ST_FT0_m100", 5000, 0.0, 5000.0); h_ST_FT0_m100->Sumw2();
  TH1D *h_ST_FT0_m50 = new TH1D("h_ST_FT0_m50", "h_ST_FT0_m50", 5000, 0.0, 5000.0); h_ST_FT0_m50->Sumw2();
  TH1D *h_ST_FT0_m10 = new TH1D("h_ST_FT0_m10", "h_ST_FT0_m10", 5000, 0.0, 5000.0); h_ST_FT0_m10->Sumw2();
  TH1D *h_ST_FT0_p10 = new TH1D("h_ST_FT0_p10", "h_ST_FT0_p10", 5000, 0.0, 5000.0); h_ST_FT0_p10->Sumw2();
  TH1D *h_ST_FT0_p50 = new TH1D("h_ST_FT0_p50", "h_ST_FT0_p50", 5000, 0.0, 5000.0); h_ST_FT0_p50->Sumw2();
  TH1D *h_ST_FT0_p100 = new TH1D("h_ST_FT0_p100", "h_ST_FT0_p100", 5000, 0.0, 5000.0); h_ST_FT0_p100->Sumw2();

  TH1D *h_m6l_FT8_m100 = new TH1D("h_m6l_FT8_m100", "h_m6l_FT8_m100", 5000, 0.0, 5000.0); h_m6l_FT8_m100->Sumw2();
  TH1D *h_m6l_FT8_m50 = new TH1D("h_m6l_FT8_m50", "h_m6l_FT8_m50", 5000, 0.0, 5000.0); h_m6l_FT8_m50->Sumw2();
  TH1D *h_m6l_FT8_m10 = new TH1D("h_m6l_FT8_m10", "h_m6l_FT8_m10", 5000, 0.0, 5000.0); h_m6l_FT8_m10->Sumw2();
  TH1D *h_m6l_FT8_p10 = new TH1D("h_m6l_FT8_p10", "h_m6l_FT8_p10", 5000, 0.0, 5000.0); h_m6l_FT8_p10->Sumw2();
  TH1D *h_m6l_FT8_p50 = new TH1D("h_m6l_FT8_p50", "h_m6l_FT8_p50", 5000, 0.0, 5000.0); h_m6l_FT8_p50->Sumw2();
  TH1D *h_m6l_FT8_p100 = new TH1D("h_m6l_FT8_p100", "h_m6l_FT8_p100", 5000, 0.0, 5000.0); h_m6l_FT8_p100->Sumw2();

  TH1D *h_ST_FT8_m100 = new TH1D("h_ST_FT8_m100", "h_ST_FT8_m100", 5000, 0.0, 5000.0); h_ST_FT8_m100->Sumw2();
  TH1D *h_ST_FT8_m50 = new TH1D("h_ST_FT8_m50", "h_ST_FT8_m50", 5000, 0.0, 5000.0); h_ST_FT8_m50->Sumw2();
  TH1D *h_ST_FT8_m10 = new TH1D("h_ST_FT8_m10", "h_ST_FT8_m10", 5000, 0.0, 5000.0); h_ST_FT8_m10->Sumw2();
  TH1D *h_ST_FT8_p10 = new TH1D("h_ST_FT8_p10", "h_ST_FT8_p10", 5000, 0.0, 5000.0); h_ST_FT8_p10->Sumw2();
  TH1D *h_ST_FT8_p50 = new TH1D("h_ST_FT8_p50", "h_ST_FT8_p50", 5000, 0.0, 5000.0); h_ST_FT8_p50->Sumw2();
  TH1D *h_ST_FT8_p100 = new TH1D("h_ST_FT8_p100", "h_ST_FT8_p100", 5000, 0.0, 5000.0); h_ST_FT8_p100->Sumw2();

  TH1D *h_m6l_FT9_m100 = new TH1D("h_m6l_FT9_m100", "h_m6l_FT9_m100", 5000, 0.0, 5000.0); h_m6l_FT9_m100->Sumw2();
  TH1D *h_m6l_FT9_m50 = new TH1D("h_m6l_FT9_m50", "h_m6l_FT9_m50", 5000, 0.0, 5000.0); h_m6l_FT9_m50->Sumw2();
  TH1D *h_m6l_FT9_m10 = new TH1D("h_m6l_FT9_m10", "h_m6l_FT9_m10", 5000, 0.0, 5000.0); h_m6l_FT9_m10->Sumw2();
  TH1D *h_m6l_FT9_p10 = new TH1D("h_m6l_FT9_p10", "h_m6l_FT9_p10", 5000, 0.0, 5000.0); h_m6l_FT9_p10->Sumw2();
  TH1D *h_m6l_FT9_p50 = new TH1D("h_m6l_FT9_p50", "h_m6l_FT9_p50", 5000, 0.0, 5000.0); h_m6l_FT9_p50->Sumw2();
  TH1D *h_m6l_FT9_p100 = new TH1D("h_m6l_FT9_p100", "h_m6l_FT9_p100", 5000, 0.0, 5000.0); h_m6l_FT9_p100->Sumw2();

  TH1D *h_ST_FT9_m100 = new TH1D("h_ST_FT9_m100", "h_ST_FT9_m100", 5000, 0.0, 5000.0); h_ST_FT9_m100->Sumw2();
  TH1D *h_ST_FT9_m50 = new TH1D("h_ST_FT9_m50", "h_ST_FT9_m50", 5000, 0.0, 5000.0); h_ST_FT9_m50->Sumw2();
  TH1D *h_ST_FT9_m10 = new TH1D("h_ST_FT9_m10", "h_ST_FT9_m10", 5000, 0.0, 5000.0); h_ST_FT9_m10->Sumw2();
  TH1D *h_ST_FT9_p10 = new TH1D("h_ST_FT9_p10", "h_ST_FT9_p10", 5000, 0.0, 5000.0); h_ST_FT9_p10->Sumw2();
  TH1D *h_ST_FT9_p50 = new TH1D("h_ST_FT9_p50", "h_ST_FT9_p50", 5000, 0.0, 5000.0); h_ST_FT9_p50->Sumw2();
  TH1D *h_ST_FT9_p100 = new TH1D("h_ST_FT9_p100", "h_ST_FT9_p100", 5000, 0.0, 5000.0); h_ST_FT9_p100->Sumw2();

  TH1D *h_eff_events = (TH1D*) inputFile->Get("Root__h_Common_LHEWeight_mg_reweighting_times_genWeight");
  double n_eff_events = h_eff_events->GetBinContent(1);
  std::cout << "n_eff_events = " << n_eff_events << std::endl; 

  int nEvents=tree->GetEntries();
  std::cout << "Reading events = " << nEvents << std::endl;

  for (int i=0; i<nEvents; ++i)
  {
    tree->GetEvent(i);
    
    float constWeight = 0.01398*1000*137.0/n_eff_events; 
    //float constWeight = 0.000190*1000*137.0/n_eff_events;  
    //std::cout << "LHEWeightmgreweighting->at(0) = " << LHEWeightmgreweighting->at(0) << std::endl;
    float weightSM = LHEWeightmgreweighting->at(0)*constWeight;
    float weightFT0_m100 = LHEWeightmgreweighting->at(1)*constWeight;
    float weightFT0_m50 = LHEWeightmgreweighting->at(2)*constWeight;
    float weightFT0_m10 = LHEWeightmgreweighting->at(3)*constWeight;
    float weightFT0_p10 = LHEWeightmgreweighting->at(4)*constWeight;
    float weightFT0_p50 = LHEWeightmgreweighting->at(5)*constWeight;
    float weightFT0_p100 = LHEWeightmgreweighting->at(6)*constWeight;

    float weightFT8_m100 = LHEWeightmgreweighting->at(7)*constWeight;
    float weightFT8_m50 = LHEWeightmgreweighting->at(8)*constWeight;
    float weightFT8_m10 = LHEWeightmgreweighting->at(9)*constWeight;
    float weightFT8_p10 = LHEWeightmgreweighting->at(10)*constWeight;
    float weightFT8_p50 = LHEWeightmgreweighting->at(11)*constWeight;
    float weightFT8_p100 = LHEWeightmgreweighting->at(12)*constWeight;

    float weightFT9_m100 = LHEWeightmgreweighting->at(13)*constWeight;
    float weightFT9_m50 = LHEWeightmgreweighting->at(14)*constWeight;
    float weightFT9_m10 = LHEWeightmgreweighting->at(15)*constWeight;
    float weightFT9_p10 = LHEWeightmgreweighting->at(16)*constWeight;
    float weightFT9_p50 = LHEWeightmgreweighting->at(17)*constWeight;
    float weightFT9_p100 = LHEWeightmgreweighting->at(18)*constWeight;

    h_m6l_SM->Fill(m6l, weightSM);
    h_m6l_FT0_m100->Fill(m6l, weightFT0_m100);
    h_m6l_FT0_m50->Fill(m6l, weightFT0_m50);
    h_m6l_FT0_m10->Fill(m6l, weightFT0_m10);
    h_m6l_FT0_p10->Fill(m6l, weightFT0_p10);
    h_m6l_FT0_p50->Fill(m6l, weightFT0_p50);
    h_m6l_FT0_p100->Fill(m6l, weightFT0_p100);
    
    h_ST_SM->Fill(ST, weightSM);
    h_ST_FT0_m100->Fill(ST, weightFT0_m100);
    h_ST_FT0_m50->Fill(ST, weightFT0_m50);
    h_ST_FT0_m10->Fill(ST, weightFT0_m10);
    h_ST_FT0_p10->Fill(ST, weightFT0_p10);
    h_ST_FT0_p50->Fill(ST, weightFT0_p50);
    h_ST_FT0_p100->Fill(ST, weightFT0_p100);
  
    h_m6l_FT8_m100->Fill(m6l, weightFT8_m100);
    h_m6l_FT8_m50->Fill(m6l, weightFT8_m50);
    h_m6l_FT8_m10->Fill(m6l, weightFT8_m10);
    h_m6l_FT8_p10->Fill(m6l, weightFT8_p10);
    h_m6l_FT8_p50->Fill(m6l, weightFT8_p50);
    h_m6l_FT8_p100->Fill(m6l, weightFT8_p100);

    h_ST_FT8_m100->Fill(ST, weightFT8_m100);
    h_ST_FT8_m50->Fill(ST, weightFT8_m50);
    h_ST_FT8_m10->Fill(ST, weightFT8_m10);
    h_ST_FT8_p10->Fill(ST, weightFT8_p10);
    h_ST_FT8_p50->Fill(ST, weightFT8_p50);
    h_ST_FT8_p100->Fill(ST, weightFT8_p100);

    h_m6l_FT9_m100->Fill(m6l, weightFT9_m100);
    h_m6l_FT9_m50->Fill(m6l, weightFT9_m50);
    h_m6l_FT9_m10->Fill(m6l, weightFT9_m10);
    h_m6l_FT9_p10->Fill(m6l, weightFT9_p10);
    h_m6l_FT9_p50->Fill(m6l, weightFT9_p50);
    h_m6l_FT9_p100->Fill(m6l, weightFT9_p100);

    h_ST_FT9_m100->Fill(ST, weightFT9_m100);
    h_ST_FT9_m50->Fill(ST, weightFT9_m50);
    h_ST_FT9_m10->Fill(ST, weightFT9_m10);
    h_ST_FT9_p10->Fill(ST, weightFT9_p10);
    h_ST_FT9_p50->Fill(ST, weightFT9_p50);
    h_ST_FT9_p100->Fill(ST, weightFT9_p100);

    h_nEvents_SM->Fill(1, weightSM);
    h_nEvents_FT0_m100->Fill(1, weightFT0_m100);
    h_nEvents_FT0_m50->Fill(1, weightFT0_m50);
    h_nEvents_FT0_m10->Fill(1, weightFT0_m10);
    h_nEvents_FT0_p10->Fill(1, weightFT0_p10);
    h_nEvents_FT0_p50->Fill(1, weightFT0_p50);
    h_nEvents_FT0_p100->Fill(1, weightFT0_p100);
 
    h_nEvents_FT8_m100->Fill(1, weightFT8_m100);
    h_nEvents_FT8_m50->Fill(1, weightFT8_m50);
    h_nEvents_FT8_m10->Fill(1, weightFT8_m10);
    h_nEvents_FT8_p10->Fill(1, weightFT8_p10);
    h_nEvents_FT8_p50->Fill(1, weightFT8_p50);
    h_nEvents_FT8_p100->Fill(1, weightFT8_p100); 

    h_nEvents_FT9_m100->Fill(1, weightFT9_m100);
    h_nEvents_FT9_m50->Fill(1, weightFT9_m50);
    h_nEvents_FT9_m10->Fill(1, weightFT9_m10);
    h_nEvents_FT9_p10->Fill(1, weightFT9_p10);
    h_nEvents_FT9_p50->Fill(1, weightFT9_p50);
    h_nEvents_FT9_p100->Fill(1, weightFT9_p100);

    if(ST > 250)
    {
      h_nEvents_SM->Fill(2, weightSM);
      h_nEvents_FT0_m100->Fill(2, weightFT0_m100);
      h_nEvents_FT0_m50->Fill(2, weightFT0_m50);
      h_nEvents_FT0_m10->Fill(2, weightFT0_m10);
      h_nEvents_FT0_p10->Fill(2, weightFT0_p10);
      h_nEvents_FT0_p50->Fill(2, weightFT0_p50);
      h_nEvents_FT0_p100->Fill(2, weightFT0_p100);

      h_nEvents_FT8_m100->Fill(2, weightFT8_m100);
      h_nEvents_FT8_m50->Fill(2, weightFT8_m50);
      h_nEvents_FT8_m10->Fill(2, weightFT8_m10);
      h_nEvents_FT8_p10->Fill(2, weightFT8_p10);
      h_nEvents_FT8_p50->Fill(2, weightFT8_p50);
      h_nEvents_FT8_p100->Fill(2, weightFT8_p100);

      h_nEvents_FT9_m100->Fill(2, weightFT9_m100);
      h_nEvents_FT9_m50->Fill(2, weightFT9_m50);
      h_nEvents_FT9_m10->Fill(2, weightFT9_m10);
      h_nEvents_FT9_p10->Fill(2, weightFT9_p10);
      h_nEvents_FT9_p50->Fill(2, weightFT9_p50);
      h_nEvents_FT9_p100->Fill(2, weightFT9_p100);  

    }
    if(ST > 1000)
    {
      h_nEvents_SM->Fill(3, weightSM);
      h_nEvents_FT0_m100->Fill(3, weightFT0_m100);
      h_nEvents_FT0_m50->Fill(3, weightFT0_m50);
      h_nEvents_FT0_m10->Fill(3, weightFT0_m10);
      h_nEvents_FT0_p10->Fill(3, weightFT0_p10);
      h_nEvents_FT0_p50->Fill(3, weightFT0_p50);
      h_nEvents_FT0_p100->Fill(3, weightFT0_p100);

      h_nEvents_FT8_m100->Fill(3, weightFT8_m100);
      h_nEvents_FT8_m50->Fill(3, weightFT8_m50);
      h_nEvents_FT8_m10->Fill(3, weightFT8_m10);
      h_nEvents_FT8_p10->Fill(3, weightFT8_p10);
      h_nEvents_FT8_p50->Fill(3, weightFT8_p50);
      h_nEvents_FT8_p100->Fill(3, weightFT8_p100);

      h_nEvents_FT9_m100->Fill(3, weightFT9_m100);
      h_nEvents_FT9_m50->Fill(3, weightFT9_m50);
      h_nEvents_FT9_m10->Fill(3, weightFT9_m10);
      h_nEvents_FT9_p10->Fill(3, weightFT9_p10);
      h_nEvents_FT9_p50->Fill(3, weightFT9_p50);
      h_nEvents_FT9_p100->Fill(3, weightFT9_p100);

    }    

  } 

  std::string histfilename=("output_"+infile+".root").c_str();
  TFile *tFile=new TFile(histfilename.c_str(), "RECREATE");
  h_m6l_SM->Write();
  h_m6l_FT0_m100->Write();
  h_m6l_FT0_m50->Write();
  h_m6l_FT0_m10->Write();
  h_m6l_FT0_p10->Write();
  h_m6l_FT0_p50->Write();
  h_m6l_FT0_p100->Write();
  
  h_ST_SM->Write();
  h_ST_FT0_m100->Write();
  h_ST_FT0_m50->Write();
  h_ST_FT0_m10->Write();
  h_ST_FT0_p10->Write();
  h_ST_FT0_p50->Write();
  h_ST_FT0_p100->Write();  

  h_m6l_FT8_m100->Write();
  h_m6l_FT8_m50->Write();
  h_m6l_FT8_m10->Write();
  h_m6l_FT8_p10->Write();
  h_m6l_FT8_p50->Write();
  h_m6l_FT8_p100->Write();
  
  h_ST_FT8_m100->Write();
  h_ST_FT8_m50->Write();
  h_ST_FT8_m10->Write();
  h_ST_FT8_p10->Write();
  h_ST_FT8_p50->Write();
  h_ST_FT8_p100->Write();

  h_m6l_FT9_m100->Write();
  h_m6l_FT9_m50->Write();
  h_m6l_FT9_m10->Write();
  h_m6l_FT9_p10->Write();
  h_m6l_FT9_p50->Write();
  h_m6l_FT9_p100->Write();
  
  h_ST_FT9_m100->Write();
  h_ST_FT9_m50->Write();
  h_ST_FT9_m10->Write();
  h_ST_FT9_p10->Write();
  h_ST_FT9_p50->Write();
  h_ST_FT9_p100->Write();

  h_nEvents_SM->Write();
  h_nEvents_FT0_m100->Write();
  h_nEvents_FT0_m50->Write();
  h_nEvents_FT0_m10->Write();
  h_nEvents_FT0_p10->Write();
  h_nEvents_FT0_p50->Write();
  h_nEvents_FT0_p100->Write();
  
  h_nEvents_FT8_m100->Write();
  h_nEvents_FT8_m50->Write();
  h_nEvents_FT8_m10->Write();
  h_nEvents_FT8_p10->Write();
  h_nEvents_FT8_p50->Write();
  h_nEvents_FT8_p100->Write();

  h_nEvents_FT9_m100->Write();
  h_nEvents_FT9_m50->Write();
  h_nEvents_FT9_m10->Write();
  h_nEvents_FT9_p10->Write();
  h_nEvents_FT9_p50->Write();
  h_nEvents_FT9_p100->Write();

  tFile->Close();
  inputFile->Close();
  std::cout<<"Wrote output file "<<histfilename<<std::endl;

  return 0;
}
  
