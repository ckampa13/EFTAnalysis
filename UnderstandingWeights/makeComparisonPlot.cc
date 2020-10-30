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
#include <TRandom.h>
#include <TCanvas.h>
#include "TPaveStats.h"

using std::string;

void makeComparisonPlot()
{

  gROOT->SetStyle("Plain");
  TCanvas c1("c1","Stacked Histogram",10,10,700,800);
  c1.SetLogy();

  TFile* file0 = new TFile("test_1.root");
  TH1F *h0 = (TH1F*)file0->Get("M_www_sm");
  h0->Rebin(10);
  h0->GetXaxis()->SetRangeUser(0.0, 3000);
  h0->SetStats(kFALSE);
  h0->SetTitle("");
  h0->GetXaxis()->SetTitle("M_{www} [GeV]");
  h0->Scale(0.209*1000*137.0/32224.0); 
  h0->SetLineWidth(2);
  h0->SetLineColor(kBlue);
  h0->Draw("HIST");

  /*TH1F *h1 = (TH1F*)file0->Get("M_www_cWm05");
  h1->Rebin(10);
  h1->Scale(0.209*1000*137.0/32224.0);
  h1->GetXaxis()->SetRangeUser(0.0, 3000);
  h1->SetLineWidth(2);
  h1->SetLineColor(kBlack);
  h1->Draw("SAME HIST");
*/
  TH1F *h2 = (TH1F*)file0->Get("M_www_cWp05");
  h2->Rebin(10);
  h2->Scale(0.209*1000*137.0/32224.0);
  h2->GetXaxis()->SetRangeUser(0.0, 3000);
  h2->SetLineWidth(2);
  h2->SetLineColor(kRed);
  h2->Draw("SAME HIST");
  
  TH1F *h1 = (TH1F*)file0->Get("M_www_cWp1");
  h1->Rebin(10);
  h1->Scale(0.209*1000*137.0/32224.0);
  h1->SetLineWidth(2);
  h1->SetLineColor(kBlack);
  h1->Draw("SAME HIST");

  TH1F *h3 = (TH1F*)file0->Get("M_www_cWp5");
  h3->Rebin(10);
  h3->Scale(0.209*1000*137.0/32224.0);
  h3->SetLineWidth(2);
  h3->SetLineColor(kMagenta);
  h3->Draw("SAME HIST");

  TLegend *leg1 = new TLegend(0.60,0.70,0.85,0.89,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.033);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(1);
  leg1->SetLineWidth(2);
  leg1->SetFillColor(0);
  leg1->SetFillStyle(1001);
  leg1->AddEntry(h0,"SM", "l");
  leg1->AddEntry(h2,"c_{w}/#Lambda^{2}: 0.05", "l");
  leg1->AddEntry(h1,"c_{w}/#Lambda^{2}: 0.1", "l");
  leg1->AddEntry(h3,"c_{w}/#Lambda^{2}: 0.5", "l");
  leg1->Draw();

  c1.SaveAs("test.png");
  c1.SaveAs("test.pdf");
}
