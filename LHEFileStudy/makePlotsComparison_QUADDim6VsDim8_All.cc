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
  c1.SetLogy();

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
  double onshell_crosssection = 1.513728154e-05*60.0*1000.0;
  double onshell_crosssection_int = 0.000867438234*1000.0; 
  double onshell_crosssection_bsm = 0.0072163*1000.0; //0.0068372*1000.0;//0.007216*1000.0
  double onshell_crosssection_sm = 0.112788441*1000.0; 

  TFile* fileOnshellAll = new TFile("test_unweighted_events_cW_01_DoubleInsertion.root");
  TH1F *hOnshellAll = (TH1F*)fileOnshellAll->Get("M_www");
  hOnshellAll->SetTitle("");
  hOnshellAll->SetLineColor(kRed);
  hOnshellAll->SetLineWidth(2);
  hOnshellAll->Rebin(20);
  hOnshellAll->GetXaxis()->SetRangeUser(0.0, 10000.0);
  hOnshellAll->SetStats(kFALSE);
  hOnshellAll->Scale(onshell_crosssection*lumi/numberOfevents);
  hOnshellAll->SetFillColor(kRed);
  hOnshellAll->SetFillStyle(3004);
  hOnshellAll->SetMaximum(5.0*hOnshellAll->GetMaximum());
  hOnshellAll->SetMinimum(1.0);
  hOnshellAll->GetYaxis()->SetTitleOffset(1.3);
  hOnshellAll->GetXaxis()->SetTitleOffset(1.3);
  hOnshellAll->GetXaxis()->SetTitle("M_www [GeV]");
  hOnshellAll->GetYaxis()->SetTitle("Events");
  hOnshellAll->Draw("HIST");

  TFile* fileOnshellBSM = new TFile("test_unweighted_events_WWW_Onshell_All_DC1.root");
  //TFile* fileOnshellBSM = new TFile("test_unweighted_events_WWW_OnShell_BSM_DSC1_Comparison.root");
  TH1F *hOnshellBSM = (TH1F*)fileOnshellBSM->Get("M_www");
  hOnshellBSM->SetLineColor(kBlue);
  hOnshellBSM->SetLineWidth(2);
  hOnshellBSM->Rebin(20);
  hOnshellBSM->GetXaxis()->SetRangeUser(0.0, 10000.0);
  hOnshellBSM->SetStats(kFALSE);
  hOnshellBSM->SetFillColor(kBlue);
  hOnshellBSM->SetFillStyle(3004);
  hOnshellBSM->Scale(onshell_crosssection_int*lumi/numberOfevents);
  //hOnshellBSM->Scale(onshell_crosssection_bsm*lumi/numberOfevents);
  hOnshellBSM->SetMaximum(1.2*hOnshellBSM->GetMaximum());
  hOnshellBSM->GetYaxis()->SetTitleOffset(1.3);
  hOnshellBSM->Draw("HIST SAME");

  TFile* fileOnshellSM = new TFile("test_unweighted_events_WWW_Onshell_SM.root");
  TH1F *hOnshellSM = (TH1F*)fileOnshellSM->Get("M_www");
  hOnshellSM->SetLineColor(kRed);
  hOnshellSM->SetLineWidth(2);
  hOnshellSM->Rebin(20);
  hOnshellSM->GetXaxis()->SetRangeUser(0.0, 10000.0);
  hOnshellSM->SetStats(kFALSE);
  hOnshellSM->SetFillColor(kRed);
  hOnshellSM->SetFillStyle(3005);
  hOnshellSM->Scale(onshell_crosssection_sm*lumi/numberOfevents);
  hOnshellSM->GetYaxis()->SetTitleOffset(1.3);
  //hOnshellSM->Draw("HIST SAME");

  TLatex TL;
  TL.SetTextAlign(11);
  TL.SetTextSize(0.03);
  TL.SetTextFont(22);
  TL.DrawLatexNDC(0.2,0.85,("generate p p > w w w"));

  TLegend *leg1 = new TLegend(0.55,0.65,0.85,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->SetHeader("#splitline{c_{W}/#Lambda^{2} = 0.1 TeV^{-2} and}{F_{T0}/#Lambda^{4} = 1 TeV^{-4}}");
  leg1->AddEntry(hOnshellAll,"(Dim 6)^2","l");
  leg1->AddEntry(hOnshellBSM,"Dim 8","l");
  leg1->Draw();

  p_2->cd();
  p_2->SetGridy();
  TH1F *h_sum=(TH1F*)hOnshellAll->Clone("h_sum");
  h_sum->Reset();
  h_sum->Add(hOnshellBSM);
  //h_sum->Add(hOnshellSM);
  TH1F *h_ratio=(TH1F*)hOnshellAll->Clone("h_ratio");
  h_ratio->GetYaxis()->SetLabelSize(0.1);
  h_ratio->GetYaxis()->SetTitleSize(0.1);
  h_ratio->GetXaxis()->SetLabelSize(0.1);
  h_ratio->GetXaxis()->SetTitleSize(0.1);
  h_ratio->GetYaxis()->SetTitleOffset(0.4);
  h_ratio->GetXaxis()->SetTitleOffset(0.9);
  h_ratio->SetTitle("; #bf{M_{WWW} (GeV)}; Full/Sum Ratio");
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

  c1.SaveAs("mass_elnu_BW_simpleComparison_QUADDim6VsDim8_Int.png");
  c1.SaveAs("mass_elnu_BW_simpleComparison_QUADDim6VsDim8_Int.pdf");
}

