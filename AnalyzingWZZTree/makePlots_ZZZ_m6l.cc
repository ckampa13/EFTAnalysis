#include <TF1.h>
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
#include <TVector3.h>
#include <TGraph.h>
#include <TRandom.h>
#include <TMath.h>
#include "Riostream.h"
#include "TCanvas.h"
#include "TPaveStats.h"
#include "TStyle.h"
#include "TLatex.h"

void makePlots()
{

  gROOT->SetStyle("Plain");
  TCanvas c1("c1","PlotsForTexFile", 10, 10, 600, 400);
  gStyle->SetOptFit(1);
  c1.SetLogy();

  TFile* file_new = TFile::Open("output_my_output_ZZZ_EFT.root");
  TH1F *h_m6l_SM = (TH1F*)file_new->Get("h_m6l_SM");
  h_m6l_SM->Rebin(100);
  h_m6l_SM->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_SM->SetMaximum(1000000);
  h_m6l_SM->SetMinimum(1.0);
  h_m6l_SM->SetStats(kFALSE); 
  h_m6l_SM->SetLineColor(kBlack);
  h_m6l_SM->SetLineWidth(2); 
  h_m6l_SM->SetTitle("");
  h_m6l_SM->GetXaxis()->SetTitle("M_{6l} [GeV]");
  h_m6l_SM->Draw("hist");


  TH1F *h_m6l_FT0_m100 = (TH1F*)file_new->Get("h_m6l_FT0_m100");
  h_m6l_FT0_m100->Rebin(100);
  h_m6l_FT0_m100->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_m100->SetLineColor(kBlue);
  h_m6l_FT0_m100->SetLineWidth(2);
  h_m6l_FT0_m100->Draw("hist same");

  TH1F *h_m6l_FT0_m50 = (TH1F*)file_new->Get("h_m6l_FT0_m50");
  h_m6l_FT0_m50->Rebin(100);
  h_m6l_FT0_m50->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_m50->SetLineColor(kRed);
  h_m6l_FT0_m50->SetLineWidth(2);
  h_m6l_FT0_m50->Draw("hist same");

  TH1F *h_m6l_FT0_m10 = (TH1F*)file_new->Get("h_m6l_FT0_m10");
  h_m6l_FT0_m10->Rebin(100);
  h_m6l_FT0_m10->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_m10->SetLineColor(kGreen+3);
  h_m6l_FT0_m10->SetLineWidth(2);
  h_m6l_FT0_m10->Draw("hist same");

  TH1F *h_m6l_FT0_p10 = (TH1F*)file_new->Get("h_m6l_FT0_p10");
  h_m6l_FT0_p10->Rebin(100);
  h_m6l_FT0_p10->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_p10->SetLineColor(kCyan);
  h_m6l_FT0_p10->SetLineWidth(2);
  h_m6l_FT0_p10->Draw("hist same");

  TH1F *h_m6l_FT0_p50 = (TH1F*)file_new->Get("h_m6l_FT0_p50");
  h_m6l_FT0_p50->Rebin(100);
  h_m6l_FT0_p50->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_p50->SetLineColor(kMagenta);
  h_m6l_FT0_p50->SetLineWidth(2);
  h_m6l_FT0_p50->Draw("hist same");  

  TH1F *h_m6l_FT0_p100 = (TH1F*)file_new->Get("h_m6l_FT0_p100");
  h_m6l_FT0_p100->Rebin(100);
  h_m6l_FT0_p100->GetXaxis()->SetRangeUser(0.0, 10000.0);
  h_m6l_FT0_p100->SetLineColor(kOrange);
  h_m6l_FT0_p100->SetLineWidth(2);
  h_m6l_FT0_p100->Draw("hist same");


  TLegend *leg = new TLegend(0.70,0.60,0.90,0.88,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(0);
  leg->SetLineWidth(1);
  leg->SetFillColor(10);
  leg->SetFillStyle(0);
  leg->AddEntry(h_m6l_SM,"SM","l");
  leg->AddEntry(h_m6l_FT0_m100,"FT0_m100","l");
  leg->AddEntry(h_m6l_FT0_m50,"FT0_m50","l");
  leg->AddEntry(h_m6l_FT0_m10,"FT0_m10","l");
  leg->AddEntry(h_m6l_FT0_p10,"FT0_p10","l");
  leg->AddEntry(h_m6l_FT0_p50,"FT0_p50","l");
  leg->AddEntry(h_m6l_FT0_p100,"FT0_p100","l");
  leg->Draw();
 
  c1.SaveAs("h_m6l.png");
  c1.SaveAs("h_m6l.pdf");

}
