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

  double param[13] = {-3.0, -1.5, -1.0, -0.8, -0.4, -0.2, 0.0, 0.2, 0.4, 0.8, 1.0, 1.5, 3.0};
  //double yield_signal_FT0[13] = {17.8, 5.52, 3.3, 2.64, 1.82, 1.62, 1.58, 1.62, 1.82, 2.64, 3.3, 5.52, 17.8};

  double yield_signal_FT0[13] = {16.22, 3.94, 1.72, 1.06, 0.24, 0.04, 0, 0.04, 0.24, 1.06, 1.72, 3.94, 16.22};

  double yield_bkg[7] = {0.043, 0.043, 0.043, 0.043, 0.043, 0.043, 0.043};
  double yield_signal_FT8[7] = {132.31521, 33.369236, 1.7217661, 0.37298381, 1.7344672, 33.432742, 132.44222}; 
  
  double yield_signal_FT9[7] = {33.714708, 8.7247388, 0.73778716, 0.37298381, 0.74598594, 8.7657327, 33.796696};
 
  int size = sizeof(param)/sizeof(double);
  std::cout << "size = " << size << std::endl;

  std::cout << "yield_signal_FT0[6] = " << yield_signal_FT0[6] << std::endl;

  for(int i=0; i<13; i++) 
  {
    //yield_signal_FT0[i] = yield_signal_FT0[i] - yield_signal_FT0[6];
    //std::cout << " yield_signal_FT0[i] = " <<  yield_signal_FT0[i] << std::endl;
    //yield_signal_FT8[i] = yield_signal_FT8[i] - yield_signal_FT8[3];
    //yield_signal_FT9[i] = yield_signal_FT9[i] - yield_signal_FT9[3];
    yield_bkg[i] = yield_bkg[i] + yield_signal_FT0[6];
  }

  TGraph *gr = new TGraph(13, param, yield_signal_FT0);
  gr->SetMarkerStyle(20);
  gr->SetMarkerColor(kBlue);
  gr->SetLineColor(kBlue);
  gr->SetMarkerSize(0.9);
  gr->SetTitle("");
  gr->GetXaxis()->SetTitle("Param (ft0)");
  gr->GetYaxis()->SetTitle("Normalized Yields");
  gr->Draw("ALP*"); 

  TF1 *fit_yield = new TF1("fit_yield","[0]+[1]*x+[2]*x*x", -5.0, 5.0);
  fit_yield->SetLineColor(kRed);
  fit_yield->SetLineWidth(2);
  fit_yield->SetLineStyle(9);
  gr->Fit("fit_yield", "", "", -5.0, 5.0);
  std::cout << "sm FT0 = " << fit_yield->GetParameter(0) << std::endl;
  std::cout << "int FT0 = " << fit_yield->GetParameter(1) << std::endl;
  std::cout << "bsm FT0 = " << fit_yield->GetParameter(2) << std::endl;
  std::cout << "Total bkg = " << yield_bkg[0] + yield_signal_FT0[3] << std::endl;
  c1.SaveAs("FT0.png");
  c1.SaveAs("FT0.pdf");
  
}

void makePlots_FT8()
{
    
    gROOT->SetStyle("Plain");
    TCanvas c2("c2","PlotsForTexFile", 10, 10, 600, 400);
    //gStyle->SetOptFit(1);
    //c1.SetLogy();
    
    double param[7] = {-100.0, -50.0, -10.0, 0.0, 10.0, 50.0, 100.0};
    double yield_signal_FT0[7] = {694.39587, 173.60760, 7.2411242, 0.37298381, 7.4792664, 174.79831, 696.77729};
    
    double yield_bkg[7] = {0.043, 0.043, 0.043, 0.043, 0.043, 0.043, 0.043};
    double yield_signal_FT8[7] = {132.31521, 33.369236, 1.7217661, 0.37298381, 1.7344672, 33.432742, 132.44222};
    
    double yield_signal_FT9[7] = {33.714708, 8.7247388, 0.73778716, 0.37298381, 0.74598594, 8.7657327, 33.796696};
    
    int size = sizeof(param)/sizeof(double);
    std::cout << "size = " << size << std::endl;
    
    for(int i=0; i<size; i++)
    {
        yield_signal_FT0[i] = yield_signal_FT0[i] - yield_signal_FT0[3];
        yield_signal_FT8[i] = yield_signal_FT8[i] - yield_signal_FT8[3];
        yield_signal_FT9[i] = yield_signal_FT9[i] - yield_signal_FT9[3];
        yield_bkg[i] = yield_bkg[i] + yield_signal_FT0[3];
    }
    
    TGraph *gr_1 = new TGraph(7, param, yield_signal_FT8);
    gr_1->SetMarkerStyle(20);
    gr_1->SetMarkerColor(kBlue);
    gr_1->SetLineColor(kBlue);
    gr_1->SetMarkerSize(0.9);
    gr_1->SetTitle("");
    gr_1->GetXaxis()->SetTitle("Param (ft8)");
    gr_1->GetYaxis()->SetTitle("Normalized Yields");
    gr_1->Draw("ALP*");
    
    TF1 *fit_yield_1 = new TF1("fit_yield_1","[0]+[1]*x+[2]*x*x", -250.0, 250.0);
    fit_yield_1->SetLineColor(kRed);
    fit_yield_1->SetLineWidth(2);
    fit_yield_1->SetLineStyle(9);
    gr_1->Fit("fit_yield_1", "", "", -250.0, 250.0);
   
    std::cout << "sm FT8 = " << fit_yield_1->GetParameter(0) << std::endl;
    std::cout << "int FT8 = " << fit_yield_1->GetParameter(1) << std::endl;
    std::cout << "bsm FT8 = " << fit_yield_1->GetParameter(2) << std::endl;
 
    c2.SaveAs("FT8.png");
    c2.SaveAs("FT8.pdf");
    
}

void makePlots_FT9()
{
    
    gROOT->SetStyle("Plain");
    TCanvas c3("c3","PlotsForTexFile", 10, 10, 600, 400);
    //gStyle->SetOptFit(1);
    //c1.SetLogy();
    
    double param[7] = {-100.0, -50.0, -10.0, 0.0, 10.0, 50.0, 100.0};
    double yield_signal_FT0[7] = {694.39587, 173.60760, 7.2411242, 0.37298381, 7.4792664, 174.79831, 696.77729};
    
    double yield_bkg[7] = {0.043, 0.043, 0.043, 0.043, 0.043, 0.043, 0.043};
    double yield_signal_FT8[7] = {132.31521, 33.369236, 1.7217661, 0.37298381, 1.7344672, 33.432742, 132.44222};
    
    double yield_signal_FT9[7] = {33.714708, 8.7247388, 0.73778716, 0.37298381, 0.74598594, 8.7657327, 33.796696};
    
    int size = sizeof(param)/sizeof(double);
    std::cout << "size = " << size << std::endl;
    
    for(int i=0; i<size; i++)
    {
        yield_signal_FT0[i] = yield_signal_FT0[i] - yield_signal_FT0[3];
        yield_signal_FT8[i] = yield_signal_FT8[i] - yield_signal_FT8[3];
        yield_signal_FT9[i] = yield_signal_FT9[i] - yield_signal_FT9[3];
        yield_bkg[i] = yield_bkg[i] + yield_signal_FT0[3];
    }
    
    TGraph *gr_1 = new TGraph(7, param, yield_signal_FT9);
    gr_1->SetMarkerStyle(20);
    gr_1->SetMarkerColor(kBlue);
    gr_1->SetLineColor(kBlue);
    gr_1->SetMarkerSize(0.9);
    gr_1->SetTitle("");
    gr_1->GetXaxis()->SetTitle("Param (ft9)");
    gr_1->GetYaxis()->SetTitle("Normalized Yields");
    gr_1->Draw("ALP*");
    
    TF1 *fit_yield_1 = new TF1("fit_yield_1","[0]+[1]*x+[2]*x*x", -250.0, 250.0);
    fit_yield_1->SetLineColor(kRed);
    fit_yield_1->SetLineWidth(2);
    fit_yield_1->SetLineStyle(9);
    gr_1->Fit("fit_yield_1", "", "", -250.0, 250.0);
   
    std::cout << "sm FT9 = " << fit_yield_1->GetParameter(0) << std::endl;
    std::cout << "int FT9 = " << fit_yield_1->GetParameter(1) << std::endl;
    std::cout << "bsm FT9 = " << fit_yield_1->GetParameter(2) << std::endl;
 
    c3.SaveAs("FT9.png");
    c3.SaveAs("FT9.pdf");
    
}
