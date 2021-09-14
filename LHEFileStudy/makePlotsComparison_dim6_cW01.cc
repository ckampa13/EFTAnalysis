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
#include "TLegend.h"

using std::string;
using std::cout;
using std::endl;
using std::istringstream;



void makePlots_BW()
{

  TCanvas c1("c1","Stacked Histogram",10,10,700,800);
  //c1.SetLogx();
  //c1.SetLogy();

  TPad *p_2=new TPad("p_2", "p_2", 0, 0.0, 1, 0.25);
  TPad *p_1=new TPad("p_1", "p_1", 0, 0.25, 1, 1);
  p_1->SetBottomMargin(0.00005);
  p_2->SetBottomMargin(0.2);
  p_1->SetFillStyle(4000);
  p_1->SetFrameFillColor(0);
  p_2->SetFillStyle(4000);
  p_2->SetFrameFillColor(0);
  p_1->SetLogy();
  p_1->Draw();
  p_2->Draw();
  p_1->cd();

  double numberOfevents = 100000.0;
  double lumi = 137.0;
  double onshell_crosssection = 0.0738833449072*1000.0;
  double onshell_crosssection_int = -6.02076306207e-05*1000.0; 
  double onshell_crosssection_bsm = 0.00162829515054*1000.0; //0.0068372*1000.0;//0.007216*1000.0
  double onshell_crosssection_sm = 0.073458606*1000.0; 
  /*
  double onshell_crosssection = 0.234474526542*1000.0;
  double onshell_crosssection_int = -0.000589255235593*1000.0;
  double onshell_crosssection_bsm = 0.162702984946*1000.0; //0.0068372*1000.0;//0.007216*1000.0
  double onshell_crosssection_sm = 0.073458606*1000.0;
  */

  TFile* filedim6All = new TFile("test_unweighted_events_WWW_dim6_All_cW01.root");
  TH1F *hdim6All = (TH1F*)filedim6All->Get("M_www");
  hdim6All->SetTitle("");
  hdim6All->SetLineColor(kBlack);
  hdim6All->SetLineWidth(2);
  hdim6All->Rebin(10);
  hdim6All->GetXaxis()->SetRangeUser(0.0, 5000.0);
  hdim6All->SetStats(kFALSE);
  hdim6All->Scale(onshell_crosssection*lumi/numberOfevents);
  hdim6All->SetFillColor(kBlack);
  hdim6All->SetFillStyle(3004);
  hdim6All->SetMinimum(0.2);
  hdim6All->GetYaxis()->SetTitleOffset(1.3);
  hdim6All->GetXaxis()->SetTitleOffset(1.3);
  hdim6All->GetXaxis()->SetTitle("M_www [GeV]");
  hdim6All->GetYaxis()->SetTitle("Events");
  hdim6All->Draw("HIST");

  TFile* filedim6Interference = new TFile("test_unweighted_events_WWW_dim6_Interference_cW01.root");
  TH1F *hdim6Interference = (TH1F*)filedim6Interference->Get("M_www");
  hdim6Interference->SetLineColor(kGreen+3);
  hdim6Interference->SetLineWidth(2);
  hdim6Interference->Rebin(10);
  hdim6Interference->SetFillStyle(3005);
  hdim6Interference->GetXaxis()->SetRangeUser(0.0, 5000.0);
  hdim6Interference->SetFillColor(kGreen+3);
  hdim6Interference->SetStats(kFALSE);
  hdim6Interference->Scale(onshell_crosssection_int*lumi/numberOfevents);
  hdim6Interference->GetYaxis()->SetTitleOffset(1.3);
  hdim6Interference->Draw("HIST SAME");

  TFile* filedim6BSM = new TFile("test_unweighted_events_WWW_dim6_BSM_cW01.root");
  TH1F *hdim6BSM = (TH1F*)filedim6BSM->Get("M_www");
  hdim6BSM->SetLineColor(kBlue);
  hdim6BSM->SetLineWidth(2);
  hdim6BSM->Rebin(10);
  hdim6BSM->GetXaxis()->SetRangeUser(0.0, 5000.0);
  hdim6BSM->SetStats(kFALSE);
  hdim6BSM->SetFillColor(kBlue);
  hdim6BSM->SetFillStyle(3004);
  hdim6BSM->Scale(onshell_crosssection_bsm*lumi/numberOfevents);
  hdim6BSM->GetYaxis()->SetTitleOffset(1.3);
  hdim6BSM->Draw("HIST SAME");

  TFile* filedim6SM = new TFile("test_unweighted_events_WWW_dim6_SM.root");
  TH1F *hdim6SM = (TH1F*)filedim6SM->Get("M_www");
  hdim6SM->SetLineColor(kRed);
  hdim6SM->SetLineWidth(2);
  hdim6SM->Rebin(10);
  hdim6SM->GetXaxis()->SetRangeUser(0.0, 5000.0);
  hdim6SM->SetStats(kFALSE);
  hdim6SM->SetFillColor(kRed);
  hdim6SM->SetFillStyle(3005);
  hdim6SM->Scale(onshell_crosssection_sm*lumi/numberOfevents);
  hdim6SM->GetYaxis()->SetTitleOffset(1.3);
  hdim6SM->Draw("HIST SAME");

  TLatex TL;
  TL.SetTextAlign(11);
  TL.SetTextSize(0.03);
  TL.SetTextFont(22);
  TL.DrawLatexNDC(0.2,0.85,("generate p p > w w w"));

  TLegend *leg1 = new TLegend(0.45,0.65,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->SetHeader("C_{w}/#Lambda^{2} = 1 TeV^{-2}");
  leg1->AddEntry(hdim6All,"All","l");
  leg1->AddEntry(hdim6Interference,"Interference","l");
  leg1->AddEntry(hdim6BSM,"Pure BSM","l");
  leg1->AddEntry(hdim6SM,"Pure SM","l");
  leg1->Draw();

  p_2->cd();
  p_2->SetGridy();
  TH1F *h_sum=(TH1F*)hdim6All->Clone("h_sum");
  h_sum->Reset();
  h_sum->Add(hdim6Interference);
  h_sum->Add(hdim6BSM);
  h_sum->Add(hdim6SM);
  TH1F *h_ratio=(TH1F*)hdim6All->Clone("h_ratio");
  h_ratio->GetYaxis()->SetLabelSize(0.1);
  h_ratio->GetYaxis()->SetTitleSize(0.1);
  h_ratio->GetXaxis()->SetLabelSize(0.1);
  h_ratio->GetXaxis()->SetTitleSize(0.1);
  h_ratio->GetYaxis()->SetTitleOffset(0.4);
  h_ratio->GetXaxis()->SetTitleOffset(0.9);
  h_ratio->SetTitle("; #bf{M_{www} (GeV)}; Full/Sum Ratio");
  h_ratio->SetStats(kFALSE);
  h_ratio->Divide(h_sum);
  h_ratio->SetLineColor(kBlack);
  h_ratio->SetMarkerStyle(20);
  h_ratio->SetMinimum(0.4);
  h_ratio->SetMaximum(1.5);
  h_ratio->Draw();
 
  TF1 *fit_ratio = new TF1("fit_ratio","[0]*x + [1]", 0.0, 10000.0);
  fit_ratio->SetParLimits(0,0.0,0.0000001);
  fit_ratio->SetParLimits(1,0.0, 5.0);
  fit_ratio->SetLineColor(kRed);
  fit_ratio->SetLineWidth(3);
  h_ratio->Fit("fit_ratio", "", "", 0.0, 10000.0);

  c1.SaveAs("WWW_dim6_simpleComparison_cW01.png");
  c1.SaveAs("WWW_dim6_simpleComparison_cW01.pdf");
}

