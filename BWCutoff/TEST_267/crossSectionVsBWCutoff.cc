#include "TH1.h"
#include "TTree.h"
#include "TKey.h"
#include "Riostream.h"
#include <TCanvas.h>
#include <TLatex.h>
#include "TGraphErrors.h"
#include "TLegend.h"
#include <TPad.h>
#include <sstream>
#include "TVectorD.h"
#include "TGraph.h"
#include "TFile.h"
#include "THStack.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TF1.h"
#include "TColor.h"

using std::string;
using std::cout;
using std::endl;
using std::istringstream;

double BR = (0.33*0.33*0.67*3 + 0.33*0.33*0.33);

void crossSectionVsBWCutOff()
{

  TCanvas c1("c1","kLong energy versus hits", 10, 10, 600, 400);
  //gStyle->SetOptFit(1);
  gROOT->SetStyle("Plain");
  gStyle->SetPadGridX(kTRUE);
  gStyle->SetPadGridY(kTRUE);
  c1.SetLogx();
  c1.SetGrid();


  double bwcutoff[13] = {1.00, 5.00, 10.00, 15.00, 20.00, 21.00, 22.00, 23.00, 24.00, 25.00, 30.00, 100.00, 100000.00}; 
  double bwcutoffError[13] = {0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00}; 
  double crosssection[13] = {0.00574, 0.007632, 0.007884, 0.007969, 0.008815955, 0.009223319, 0.009623585, 0.009978861, 0.01032548, 0.010663964, 0.0118283523288, 0.012619523053, 0.012605527586};
  double crosssectionError[13] = {4.3e-06, 5.4e-06, 5.8e-06, 5.7e-06, 6.4e-06, 6.9e-06, 7.0e-06, 7.4e-06, 7.6e-06, 8.0e-06, 8.3e-06, 9.3e-06, 9.6e-06};
  
  /*double bwcutoff[11] = {1.00, 5.00, 10.00, 15.00, 20.00, 21.00, 22.00, 23.00, 24.00, 25.00, 30.00};
  double bwcutoffError[11] = {0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00};
  double crosssection[11] = {0.00574, 0.007632, 0.007884, 0.007969, 0.008815955, 0.009223319, 0.009623585, 0.009978861, 0.01032548, 0.010663964, 0.0118283523288};
  double crosssectionError[11] = {4.3e-06, 5.4e-06, 5.8e-06, 5.7e-06, 6.4e-06, 6.9e-06, 7.0e-06, 7.4e-06, 7.6e-06, 8.0e-06, 8.3e-06};
  */
  int npoints = sizeof(bwcutoff)/sizeof(double);

  TGraphErrors *gr1obs = new TGraphErrors(npoints, bwcutoff, crosssection, bwcutoffError, crosssectionError);
  gr1obs->SetLineStyle(5);
  gr1obs->SetLineColor(kRed);
  gr1obs->SetLineWidth(2);
  gr1obs->SetMarkerColor(kRed);
  gr1obs->SetTitle("");
  gr1obs->GetXaxis()->SetTitle("BWCutoff");
  gr1obs->GetYaxis()->CenterTitle();
  gr1obs->GetYaxis()->SetTitleOffset(1.3);
  gr1obs->GetYaxis()->SetTitle("Cross section [pb]");
  //gr1obs->SetMaximum(0.013);
  //gr1obs->SetMinimum(0.0);
  gr1obs->Draw("APL* e");

  TLegend *leg = new TLegend(0.25,0.25,0.60,0.35,NULL,"brNDC");
  leg->AddEntry(gr1obs, "Cross section", "l");
  leg->SetFillColor(0);
  leg->SetBorderSize(0);
  leg->Draw();

  TLatex TL;
  TL.SetTextAlign(11);
  TL.SetTextSize(0.05);
  TL.SetTextFont(22);
  TL.DrawLatexNDC(0.25,0.94,"BW Cutoff versus cross section");
  

  c1.SaveAs("crosssection_bwcutoff.pdf");
  c1.SaveAs("crosssection_bwcutoff.png");  
   

} 
