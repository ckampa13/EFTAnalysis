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

void makePlots_FT0()
{

  gROOT->SetStyle("Plain");
  TCanvas c1("c1","PlotsForTexFile", 10, 10, 600, 400);
  //gStyle->SetOptFit(1);
  //c1.SetLogy();

  TF1 *fit_yield = new TF1("fit_yield","1+0.04*x+0.5*x*x", -5.0, 5.0);
  fit_yield->SetLineColor(kRed);
  fit_yield->SetLineWidth(2);
  fit_yield->SetLineStyle(9);
  fit_yield->SetTitle("");
  fit_yield->Draw("");

  TF1 *fit_yield_two = new TF1("fit_yield_two","1+0.04*x+1.0*x*x", -5.0, 5.0);
  fit_yield_two->SetLineColor(kBlue);
  fit_yield_two->SetLineWidth(2);
  fit_yield_two->SetLineStyle(9);
  fit_yield_two->Draw("same");


  TF1 *fit_yield_three = new TF1("fit_yield_three","1+0.4*x+1.0*x*x", -5.0, 5.0);
  fit_yield_three->SetLineColor(kGreen+3);
  fit_yield_three->SetLineWidth(2);
  fit_yield_three->SetLineStyle(9);
  fit_yield_three->Draw("same");


  c1.SaveAs("par1.png");
  c1.SaveAs("par1.pdf");

}

void makePlots_FT0_png()
{

  gROOT->SetStyle("Plain");
  TCanvas c1("c1","PlotsForTexFile", 10, 10, 600, 400);
  //gStyle->SetOptFit(1);
  //c1.SetLogy();

  TF1 *fit_yield = new TF1("fit_yield","1-0.04*x+0.5*x*x", -5.0, 5.0);
  fit_yield->SetLineColor(kRed);
  fit_yield->SetLineWidth(2);
  fit_yield->SetLineStyle(9);
  fit_yield->SetTitle("");
  fit_yield->Draw("");

   
  TF1 *fit_yield_two = new TF1("fit_yield_two","1-0.04*x+1.0*x*x", -5.0, 5.0);
  fit_yield_two->SetLineColor(kBlue);
  fit_yield_two->SetLineWidth(2);
  fit_yield_two->SetLineStyle(9);
  fit_yield_two->Draw("same");


  TF1 *fit_yield_three = new TF1("fit_yield_three","1-0.4*x+1.0*x*x", -5.0, 5.0);
  fit_yield_three->SetLineColor(kGreen+3);
  fit_yield_three->SetLineWidth(2);
  fit_yield_three->SetLineStyle(9);
  fit_yield_three->Draw("same");


  c1.SaveAs("par2.png");
  c1.SaveAs("par2.pdf");

}
  
