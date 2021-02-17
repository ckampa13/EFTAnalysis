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

  double lumi = 137.0;
  double numberOfevents = 100000.0;

  TFile* fileWWW_Onshell_BW1 = new TFile("test_WWWOnshell_bw1.root");
  TH1F *hWWW_Onshell_BW1 = (TH1F*)fileWWW_Onshell_BW1->Get("h_el_pT");
  hWWW_Onshell_BW1->SetLineColor(kRed);
  hWWW_Onshell_BW1->SetLineWidth(2);
  hWWW_Onshell_BW1->Rebin(5);
  hWWW_Onshell_BW1->GetXaxis()->SetRangeUser(0.0, 300.0);
  if(hWWW_Onshell_BW1->Integral() > 0.0) hWWW_Onshell_BW1->Scale(1.0/hWWW_Onshell_BW1->Integral());
  //hWWW_Onshell_BW1->Scale(0.00574*lumi/numberOfevents);
  hWWW_Onshell_BW1->SetStats(kFALSE);
  hWWW_Onshell_BW1->SetTitle("");
  hWWW_Onshell_BW1->GetYaxis()->SetTitleOffset(1.3);
  hWWW_Onshell_BW1->GetXaxis()->SetTitleOffset(1.3);
  hWWW_Onshell_BW1->GetXaxis()->SetTitle("Electron pT [GeV]");
  //hWWW_Onshell_BW1->GetXaxis()->SetTitle("#splitline{Mass of the W boson}{(electron + neutrino invariant mass) [GeV]}");
  hWWW_Onshell_BW1->GetYaxis()->SetTitle("A.U.");
  //hWWW_Onshell_BW1->SetMaximum(1.0);
  hWWW_Onshell_BW1->SetMinimum(0.0001);
  hWWW_Onshell_BW1->Draw("HIST");

  TFile* fileWWW_Onshell_BW5= new TFile("test_WWWOnshell_bw5.root");
  TH1F *hWWW_Onshell_BW5= (TH1F*)fileWWW_Onshell_BW5->Get("h_el_pT");
  hWWW_Onshell_BW5->SetLineColor(kBlue);
  hWWW_Onshell_BW5->SetLineWidth(2);
  hWWW_Onshell_BW5->Rebin(5);
  //hWWW_Onshell_BW5->Scale(0.007632*lumi/numberOfevents);
  if(hWWW_Onshell_BW5->Integral() > 0.0) hWWW_Onshell_BW5->Scale(1.0/hWWW_Onshell_BW5->Integral());
  hWWW_Onshell_BW5->Draw("HIST SAME");

  TFile* fileWWW_Onshell_BW10= new TFile("test_WWWOnshell_bw10.root");
  TH1F *hWWW_Onshell_BW10= (TH1F*)fileWWW_Onshell_BW10->Get("h_el_pT");
  hWWW_Onshell_BW10->SetLineColor(kGreen+3);
  hWWW_Onshell_BW10->SetLineWidth(2);
  hWWW_Onshell_BW10->Rebin(5);
  //hWWW_Onshell_BW10->Scale(0.007884*lumi/numberOfevents);
  if(hWWW_Onshell_BW10->Integral() > 0.0) hWWW_Onshell_BW10->Scale(1.0/hWWW_Onshell_BW10->Integral());
  hWWW_Onshell_BW10->Draw("HIST SAME");

  TFile* fileWWW_Onshell_BW15 = new TFile("test_WWWOnshell_bw15.root");
  TH1F *hWWW_Onshell_BW15 = (TH1F*)fileWWW_Onshell_BW15->Get("h_el_pT");
  hWWW_Onshell_BW15->SetLineColor(kBlack);
  hWWW_Onshell_BW15->SetLineWidth(2);
  hWWW_Onshell_BW15->Rebin(5);
  //hWWW_Onshell_BW15->Scale(0.007969*lumi/numberOfevents);
  if(hWWW_Onshell_BW15->Integral() > 0.0) hWWW_Onshell_BW15->Scale(1.0/hWWW_Onshell_BW15->Integral());
  hWWW_Onshell_BW15->Draw("HIST SAME");

  TFile* fileWWW_Onshell_BW100 = new TFile("test_WWWOnshell_bw100.root");
  TH1F *hWWW_Onshell_BW100 = (TH1F*)fileWWW_Onshell_BW100->Get("h_el_pT");
  hWWW_Onshell_BW100->SetLineColor(kMagenta);
  hWWW_Onshell_BW100->SetLineWidth(2);
  hWWW_Onshell_BW100->Rebin(5);
  //hWWW_Onshell_BW100->Scale(0.012619523053*lumi/numberOfevents);
  if(hWWW_Onshell_BW100->Integral() > 0.0) hWWW_Onshell_BW100->Scale(1.0/hWWW_Onshell_BW100->Integral());
  hWWW_Onshell_BW100->Draw("HIST SAME");

  TFile* fileWWW_Onshell_BW100000 = new TFile("test_WWWOnshell_bw100000.root");
  TH1F *hWWW_Onshell_BW100000 = (TH1F*)fileWWW_Onshell_BW100000->Get("h_el_pT");
  hWWW_Onshell_BW100000->SetLineColor(kOrange-3);
  hWWW_Onshell_BW100000->SetLineWidth(2);
  hWWW_Onshell_BW100000->Rebin(5);
  //hWWW_Onshell_BW100000->Scale(0.012605527586*lumi/numberOfevents);
  if(hWWW_Onshell_BW100000->Integral() > 0.0) hWWW_Onshell_BW100000->Scale(1.0/hWWW_Onshell_BW100000->Integral());
  hWWW_Onshell_BW100000->Draw("HIST SAME");

  TLegend *leg1 = new TLegend(0.47,0.55,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->AddEntry(hWWW_Onshell_BW1,"Onshell BW cutoff: 1","l");
  leg1->AddEntry(hWWW_Onshell_BW5,"Onshell BW cutoff: 5","l");
  leg1->AddEntry(hWWW_Onshell_BW10,"Onshell BW cutoff: 10","l");
  leg1->AddEntry(hWWW_Onshell_BW15,"Onshell BW cutoff: 15","l");
  leg1->AddEntry(hWWW_Onshell_BW100,"Onshell BW cutoff: 100","l");
  leg1->AddEntry(hWWW_Onshell_BW100000,"Onshell BW cutoff: 100000","l");
  leg1->Draw();

  c1.SaveAs("h_el_pT_Onshell_AU.png");
  c1.SaveAs("h_el_pT_Onshell_AU.pdf");
}

