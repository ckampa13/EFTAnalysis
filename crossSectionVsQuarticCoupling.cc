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

void crossSectionVsQuarticCoupling()
{

  TCanvas c1("c1","kLong energy versus hits", 10, 10, 600, 400);
  //gStyle->SetOptFit(1);
  gROOT->SetStyle("Plain");
  gStyle->SetPadGridX(kTRUE);
  gStyle->SetPadGridY(kTRUE);
  c1.SetGrid();

  double quartic[14] = {1.30, 1.20, 1.10,  1.09, 1.00, 0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.90, 0.80, 0.70}; 
  double crosssection[14] = {0.8974, 0.4616, 0.2007, 0.1844, 0.1125, 0.1127, 0.116, 0.1179, 0.1203, 0.1262, 0.1341, 0.198, 0.4568, 0.8903};

  int npoints = sizeof(quartic)/sizeof(double);

  TGraph *gr1obs = new TGraph(npoints, quartic, crosssection);
  gr1obs->SetLineStyle(5);
  gr1obs->SetLineColor(kBlue);
  gr1obs->SetLineWidth(2);
  gr1obs->SetMarkerColor(kBlue);
  gr1obs->SetTitle("");
  gr1obs->GetXaxis()->SetTitle("Strength of quartic coupling");
  gr1obs->GetYaxis()->CenterTitle();
  gr1obs->GetYaxis()->SetTitleOffset(1.3);
  gr1obs->GetYaxis()->SetTitle("Cross section [pb]");
  //gr1obs->SetMaximum(0.145);
  gr1obs->SetMinimum(0.105);
  gr1obs->Draw("APL* e");

  TLegend *leg = new TLegend(0.20,0.75,0.55,0.85,NULL,"brNDC");
  leg->AddEntry(gr1obs, "Cross section", "l");
  leg->SetFillColor(0);
  leg->SetBorderSize(0);
  leg->Draw();

  TF1 *fit_yield = new TF1("fit_yield","[0]+[1]*x+[2]*x*x", 0.0, 2.0);
  fit_yield->SetLineColor(kRed);
  fit_yield->SetLineWidth(2);
  fit_yield->SetLineStyle(9);
  gr1obs->Fit("fit_yield", "", "", 1.5, 0.5);

  TLatex TL;
  TL.SetTextAlign(11);
  TL.SetTextSize(0.05);
  TL.SetTextFont(22);
  TL.DrawLatexNDC(0.25,0.94,"Strength of quartic coupling versus cross section");
  

  c1.SaveAs("crosssection_quartic.pdf");
  c1.SaveAs("crosssection_quartic.png");  
   

} 
