#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TSystem.h>
#include <TChain.h>
#include <TLorentzVector.h>
#include <TLegend.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <algorithm>
#include <TGraphAsymmErrors.h>
#include <TVector2.h>
#include <TF1.h>

using namespace std;

double MUON_MASS = 105.6583745*10e-03;
double ELECTRON_MASS = 511*10e-06;

bool sameVal(double a, double b)
{
   return fabs(a - b) < 1.000e-02;
}

TLorentzVector fillTLorentzVector(double pT, double eta, double phi, double M)
{
  TLorentzVector object_p4;
  object_p4.SetPtEtaPhiM(pT, eta, phi, M);
  return object_p4;
}

typedef struct
{
  double pT;
  double eta;
  double phi;
  int charge;
  TLorentzVector lep_lv;
} LeptonInfo;

typedef struct
{
  double pT;
  double eta;
  double phi;
} PhotonInfo;

typedef struct
{
  double pT;
  double eta;
  double phi;
  double mass;
  int btag;
} JetInfo;

typedef struct
{
  TLorentzVector JetLV;
  float BTag_CSV;
} AnalysisJetInfo; 

bool sortLeptonsInDescendingpT(LeptonInfo lep1, LeptonInfo lep2)
{
  return (lep1.pT > lep2.pT);
}

bool sortJetsInDescendingpT(JetInfo jet1, JetInfo jet2)
{
  return (jet1.pT > jet2.pT);
}

bool sortJetVectorsInDescendingpT(AnalysisJetInfo jet1, AnalysisJetInfo jet2)
{
  return (jet1.JetLV.Pt() > jet2.JetLV.Pt());
}

bool sortLepVectorsInDescendingpT(LeptonInfo lep1, LeptonInfo lep2)
{
  return (lep1.lep_lv.Pt() > lep2.lep_lv.Pt());
}

/*
bool sortJetVectorsInDescendingpT(TLorentzVector jet1, TLorentzVector jet2)
{
  return (jet1.Pt() > jet2.Pt());
}*/

bool sortPhotonsInDescendingpT(PhotonInfo pho1, PhotonInfo pho2)
{
  return (pho1.pT > pho2.pT);
}

double mT(TLorentzVector p4, float met, float met_phi)
{
  float phi1 = p4.Phi();
  float phi2 = met_phi;
  float Et1  = p4.Et();
  float Et2  = met;
  return sqrt(2*Et1*Et2*(1.0 - cos(phi1-phi2)));
}

int ReadZZZ_Delphes_6l(std::string infile, std::string outfile){

  std::string inputfilename=(infile+".root").c_str();
  TChain *tree=new TChain("LowPtSUSY_Tree");
  tree->Add(inputfilename.c_str());
  std::cout<<"Opened input file "<<inputfilename<<std::endl;

  std::vector<double>   *ph_pt;
  std::vector<double>   *ph_phi;
  vector<double>   *ph_eta;
  Int_t           nPhotons;
  vector<double>   *el_pt;
  vector<double>   *el_phi;
  vector<double>   *el_eta;
  vector<int>     *el_charge;
  Int_t           nElectrons;
  vector<double>   *mu_pt;
  vector<double>   *mu_phi;
  vector<double>   *mu_eta;
  vector<int>     *mu_charge;
  Int_t           nMuons;
  vector<double>   *jet_pt;
  vector<double>   *jet_phi;
  vector<double>   *jet_eta;
  vector<double>   *jet_mass;
  vector<int>     *jet_btag;
  Int_t           nJets;
  Float_t         MET;
  Float_t         MET_Phi;

  ph_pt = 0;
  ph_phi = 0;
  ph_eta = 0;
  el_pt = 0;
  el_phi = 0;
  el_eta = 0;
  el_charge = 0;
  mu_pt = 0;
  mu_phi = 0;
  mu_eta = 0;
  mu_charge = 0;
  jet_pt = 0;
  jet_phi = 0;
  jet_eta = 0;
  jet_mass = 0;
  jet_btag = 0;
  tree->SetBranchAddress("ph_pt", &(ph_pt));
  tree->SetBranchAddress("ph_phi", &(ph_phi));
  tree->SetBranchAddress("ph_eta", &(ph_eta));
  tree->SetBranchAddress("nPhotons", &(nPhotons));
  tree->SetBranchAddress("el_pt", &(el_pt));
  tree->SetBranchAddress("el_eta", &(el_eta));
  tree->SetBranchAddress("el_phi", &(el_phi));
  tree->SetBranchAddress("el_charge", &(el_charge));
  tree->SetBranchAddress("nElectrons", &(nElectrons));
  tree->SetBranchAddress("mu_pt", &(mu_pt));
  tree->SetBranchAddress("mu_eta", &(mu_eta));
  tree->SetBranchAddress("mu_phi", &(mu_phi));
  tree->SetBranchAddress("mu_charge", &(mu_charge));
  tree->SetBranchAddress("nMuons", &(nMuons));
  tree->SetBranchAddress("jet_pt", &(jet_pt));
  tree->SetBranchAddress("jet_phi", &(jet_phi));
  tree->SetBranchAddress("jet_eta", &(jet_eta));
  tree->SetBranchAddress("jet_mass", &(jet_mass));
  tree->SetBranchAddress("jet_btag", &(jet_btag));
  tree->SetBranchAddress("nJets", &(nJets));
  tree->SetBranchAddress("MET", &(MET));
  tree->SetBranchAddress("MET_Phi", &(MET_Phi));


  TH1F *h_sumPt = new TH1F("h_sumPt", "sumPt (scalar sum of lepton pT); sumPt [GeV]; Events/GeV", 500, 0, 5000.0);          h_sumPt->Sumw2();
  TH1F *h_Mll   = new TH1F("h_Mll", "Mll (invariant mass of the 6 lepton system); Mll [GeV]; Events/GeV", 500, 0, 6000.0);  h_Mll->Sumw2();
  TH1F *h_lep0_Pt = new TH1F("h_lep0_Pt", "Leading lepton pT; pT of the leading lepton [GeV]; Events/GeV", 1000, 0, 1000.0); h_lep0_Pt->Sumw2();
  TH1F *h_lep1_Pt = new TH1F("h_lep1_Pt", "Second lepton pT; pT of the second lepton [GeV]; Events/GeV", 1000, 0, 1000.0);  h_lep1_Pt->Sumw2();
  TH1F *h_lep2_Pt = new TH1F("h_lep2_Pt", "Third lepton pT; pT of the third lepton [GeV]; Events/GeV", 1000, 0, 1000.0);   h_lep2_Pt->Sumw2();
  TH1F *h_lep3_Pt = new TH1F("h_lep3_Pt", "Fourth lepton pT; pT of the fourth lepton [GeV]; Events/GeV", 1000, 0, 1000.0);  h_lep3_Pt->Sumw2();
  TH1F *h_lep4_Pt = new TH1F("h_lep4_Pt", "Fifth lepton pT; pT of the fifth lepton [GeV]; Events/GeV", 1000, 0, 1000.0);   h_lep4_Pt->Sumw2();
  TH1F *h_lep5_Pt = new TH1F("h_lep5_Pt", "Sixth lepton pT; pT of the sixth lepton [GeV]; Events/GeV", 1000, 0, 1000.0);   h_lep5_Pt->Sumw2();
  TH1F *h_nLeptons = new TH1F("h_nLeptons", "Number of leptons; Number of leptons; Events",  10, -0.5, 9.5); h_nLeptons->Sumw2();

  int nEvents=tree->GetEntries();
  std::cout << "nEvents= " << nEvents << std::endl;
  int n_events_PT250 = 0;
  for (int i=0; i<nEvents ; ++i)
  {
     tree->GetEvent(i);
     std::vector<LeptonInfo> leptons;
     std::vector<LeptonInfo> electrons;
     for (unsigned int j=0; j<el_pt->size(); ++j)
     {
       LeptonInfo electron;
       electron.pT=el_pt->at(j);
       electron.eta=el_eta->at(j);
       electron.phi=el_phi->at(j);
       electron.charge=el_charge->at(j);
       electron.lep_lv.SetPtEtaPhiM(el_pt->at(j), el_eta->at(j), el_phi->at(j), ELECTRON_MASS);
       electrons.push_back(electron);
       leptons.push_back(electron);
     }

     // Now sorting this vector of structs
     std::sort (electrons.begin(), electrons.end(), sortLeptonsInDescendingpT);
   
     // filling the muon's properties into a vector of struct
     std::vector<LeptonInfo> muons;
     for (unsigned int j=0; j<mu_pt->size(); ++j)
     {
       LeptonInfo muon;
       muon.pT=mu_pt->at(j);
       muon.eta=mu_eta->at(j);
       muon.phi=mu_phi->at(j);
       muon.charge=mu_charge->at(j);
       muon.lep_lv.SetPtEtaPhiM(mu_pt->at(j), mu_eta->at(j), mu_phi->at(j), MUON_MASS);
       muons.push_back(muon);
       leptons.push_back(muon);
     }
     // Now sorting this vector of structs
     std::sort (muons.begin(), muons.end(), sortLeptonsInDescendingpT);

     std::vector<JetInfo> jets;
     for (unsigned int j=0; j<jet_pt->size(); ++j)
     {
       JetInfo jet;
       jet.pT = jet_pt->at(j);
       jet.eta = jet_eta->at(j);
       jet.phi = jet_phi->at(j);
       jet.mass = jet_mass->at(j);
       jet.btag = jet_btag->at(j);
       jets.push_back(jet);
     }

     // Now sorting this vector of structs
     std::sort (jets.begin(), jets.end(), sortJetsInDescendingpT);   
     std::sort (leptons.begin(), leptons.end(), sortLepVectorsInDescendingpT);  
     h_nLeptons->Fill(leptons.size());
 
     double Mll = 0.0;
     double sumPt = 0.0;
     for(unsigned int l=0; l < leptons.size(); ++l)
     {
       if(leptons.size() >= 6) sumPt += leptons.at(l).lep_lv.Pt();
      //if(leptons.size() >= 6) sumPt += leptons.at(l).lep_lv.Pt(); 
     }
     if(sumPt > 0.0) h_sumPt->Fill(sumPt);
     if(sumPt > 250.0) n_events_PT250++;
     if(leptons.size() >= 6) Mll = (leptons.at(0).lep_lv + leptons.at(1).lep_lv + leptons.at(2).lep_lv + leptons.at(3).lep_lv + leptons.at(4).lep_lv + leptons.at(5).lep_lv).M(); 
     if(Mll>0.0) h_Mll->Fill(Mll);
     if(leptons.size() > 0) h_lep0_Pt->Fill(leptons.at(0).lep_lv.Pt());
     if(leptons.size() > 1) h_lep1_Pt->Fill(leptons.at(1).lep_lv.Pt());
     if(leptons.size() > 2) h_lep2_Pt->Fill(leptons.at(2).lep_lv.Pt());
     if(leptons.size() > 3) h_lep3_Pt->Fill(leptons.at(3).lep_lv.Pt());
     if(leptons.size() > 4) h_lep4_Pt->Fill(leptons.at(4).lep_lv.Pt());
     if(leptons.size() > 5) h_lep5_Pt->Fill(leptons.at(5).lep_lv.Pt());

  }//event loop closed

  
  std::cout << "n_events_PT250 = " << n_events_PT250 << std::endl;
  std::cout << (outfile).c_str() << "n_events_PT250_normalized = " << (n_events_PT250*37.1*137*0.06*0.06*0.06)/100000.0 << std::endl;
  std::string histfilename=(outfile+".root").c_str();
  TFile *tFile=new TFile(histfilename.c_str(), "RECREATE");
  h_lep0_Pt->Write();
  h_lep1_Pt->Write();
  h_lep2_Pt->Write();
  h_lep3_Pt->Write();
  h_lep4_Pt->Write();
  h_lep5_Pt->Write();
  h_Mll->Write();
  h_sumPt->Write();
  h_nLeptons->Write();
  tFile->Close();
  std::cout<<"Wrote output file "<<histfilename<<std::endl;
  return 0;

}
