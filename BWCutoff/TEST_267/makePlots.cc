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

void makeMassOne()
{

  TCanvas c1("c1","Stacked Histogram",10,10,700,800);
  //c1.SetLogx();
  c1.SetLogy();

  TFile* fileWWW_BW15 = new TFile("test_BW_15.root");
  TH1F *hWWW_BW15 = (TH1F*)fileWWW_BW15->Get("massW_1");
  hWWW_BW15->SetLineColor(kBlack);
  hWWW_BW15->SetLineWidth(2);
  hWWW_BW15->Rebin(5);
  hWWW_BW15->GetXaxis()->SetRangeUser(0, 350.0);
  hWWW_BW15->SetMinimum(0.1);
  hWWW_BW15->SetStats(kFALSE);
  hWWW_BW15->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW15->GetXaxis()->SetTitle("Mass of the first W boson [GeV]");
  hWWW_BW15->GetYaxis()->SetTitle("Events");
  hWWW_BW15->Draw("HIST");

  TFile* fileWWW_BW100 = new TFile("test_BW_100.root");
  TH1F *hWWW_BW100 = (TH1F*)fileWWW_BW100->Get("massW_1");
  hWWW_BW100->SetLineColor(kRed);
  hWWW_BW100->SetLineWidth(2);
  hWWW_BW100->Rebin(5);
  hWWW_BW100->GetXaxis()->SetRangeUser(0, 350.0);
  hWWW_BW100->SetStats(kFALSE);
  hWWW_BW100->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW100->Draw("HIST SAME");

  TFile* fileWWW_BW1000000 = new TFile("test_BW_1000000.root");
  TH1F *hWWW_BW1000000 = (TH1F*)fileWWW_BW1000000->Get("massW_1");
  hWWW_BW1000000->SetLineColor(kBlue);
  hWWW_BW1000000->SetLineWidth(2);
  hWWW_BW1000000->Rebin(5);
  hWWW_BW1000000->GetXaxis()->SetRangeUser(0, 350.0);
  hWWW_BW1000000->SetStats(kFALSE);
  hWWW_BW1000000->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW1000000->Draw("HIST SAME");

  TLegend *leg1 = new TLegend(0.52,0.55,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->AddEntry(hWWW_BW15,"BW cutoff: 15","l");
  leg1->AddEntry(hWWW_BW100,"BW cutoff: 100","l");
  leg1->AddEntry(hWWW_BW1000000,"BW cutoff: 1000000","l");
  leg1->Draw();

  c1.SaveAs("mass1_BW.png");
  c1.SaveAs("mass1_BW.pdf");
}

void makeMassTwo()
{
    
    TCanvas c1("c1","Stacked Histogram",10,10,700,800);
    //c1.SetLogx();
    c1.SetLogy();
    
    TFile* fileWWW_BW15 = new TFile("test_BW_15.root");
    TH1F *hWWW_BW15 = (TH1F*)fileWWW_BW15->Get("massW_2");
    hWWW_BW15->SetLineColor(kBlack);
    hWWW_BW15->SetLineWidth(2);
    hWWW_BW15->Rebin(5);
    hWWW_BW15->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW15->SetMinimum(0.1);
    hWWW_BW15->SetStats(kFALSE);
    hWWW_BW15->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW15->GetXaxis()->SetTitle("Mass of the second W boson [GeV]");
    hWWW_BW15->GetYaxis()->SetTitle("Events");
    hWWW_BW15->Draw("HIST");
    
    TFile* fileWWW_BW100 = new TFile("test_BW_100.root");
    TH1F *hWWW_BW100 = (TH1F*)fileWWW_BW100->Get("massW_2");
    hWWW_BW100->SetLineColor(kRed);
    hWWW_BW100->SetLineWidth(2);
    hWWW_BW100->Rebin(5);
    hWWW_BW100->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW100->SetStats(kFALSE);
    hWWW_BW100->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW100->Draw("HIST SAME");
    
    TFile* fileWWW_BW1000000 = new TFile("test_BW_1000000.root");
    TH1F *hWWW_BW1000000 = (TH1F*)fileWWW_BW1000000->Get("massW_2");
    hWWW_BW1000000->SetLineColor(kBlue);
    hWWW_BW1000000->SetLineWidth(2);
    hWWW_BW1000000->Rebin(5);
    hWWW_BW1000000->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW1000000->SetStats(kFALSE);
    hWWW_BW1000000->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW1000000->Draw("HIST SAME");
    
    TLegend *leg1 = new TLegend(0.52,0.55,0.80,0.82,NULL,"brNDC");
    leg1->SetBorderSize(0);
    leg1->SetTextSize(0.03);
    leg1->SetLineColor(1);
    leg1->SetLineStyle(0);
    leg1->SetLineWidth(1);
    leg1->SetFillColor(10);
    leg1->SetFillStyle(0);
    leg1->AddEntry(hWWW_BW15,"BW cutoff: 15","l");
    leg1->AddEntry(hWWW_BW100,"BW cutoff: 100","l");
    leg1->AddEntry(hWWW_BW1000000,"BW cutoff: 1000000","l");
    leg1->Draw();
    
    c1.SaveAs("mass2_BW.png");
    c1.SaveAs("mass2_BW.pdf");
}

void makeMassThree()
{
    
    TCanvas c1("c1","Stacked Histogram",10,10,700,800);
    //c1.SetLogx();
    c1.SetLogy();
    
    TFile* fileWWW_BW15 = new TFile("test_BW_15.root");
    TH1F *hWWW_BW15 = (TH1F*)fileWWW_BW15->Get("massW_3");
    hWWW_BW15->SetLineColor(kBlack);
    hWWW_BW15->SetLineWidth(2);
    hWWW_BW15->Rebin(5);
    hWWW_BW15->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW15->SetMinimum(0.1);
    hWWW_BW15->SetStats(kFALSE);
    hWWW_BW15->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW15->GetXaxis()->SetTitle("Mass of the third W boson [GeV]");
    hWWW_BW15->GetYaxis()->SetTitle("Events");
    hWWW_BW15->Draw("HIST");
    
    TFile* fileWWW_BW100 = new TFile("test_BW_100.root");
    TH1F *hWWW_BW100 = (TH1F*)fileWWW_BW100->Get("massW_3");
    hWWW_BW100->SetLineColor(kRed);
    hWWW_BW100->SetLineWidth(2);
    hWWW_BW100->Rebin(5);
    hWWW_BW100->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW100->SetStats(kFALSE);
    hWWW_BW100->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW100->Draw("HIST SAME");
    
    TFile* fileWWW_BW1000000 = new TFile("test_BW_1000000.root");
    TH1F *hWWW_BW1000000 = (TH1F*)fileWWW_BW1000000->Get("massW_3");
    hWWW_BW1000000->SetLineColor(kBlue);
    hWWW_BW1000000->SetLineWidth(2);
    hWWW_BW1000000->Rebin(5);
    hWWW_BW1000000->GetXaxis()->SetRangeUser(0, 350.0);
    hWWW_BW1000000->SetStats(kFALSE);
    hWWW_BW1000000->GetYaxis()->SetTitleOffset(1.3);
    hWWW_BW1000000->Draw("HIST SAME");
    
    TLegend *leg1 = new TLegend(0.52,0.55,0.80,0.82,NULL,"brNDC");
    leg1->SetBorderSize(0);
    leg1->SetTextSize(0.03);
    leg1->SetLineColor(1);
    leg1->SetLineStyle(0);
    leg1->SetLineWidth(1);
    leg1->SetFillColor(10);
    leg1->SetFillStyle(0);
    leg1->AddEntry(hWWW_BW15,"BW cutoff: 15","l");
    leg1->AddEntry(hWWW_BW100,"BW cutoff: 100","l");
    leg1->AddEntry(hWWW_BW1000000,"BW cutoff: 1000000","l");
    leg1->Draw();
    
    c1.SaveAs("mass3_BW.png");
    c1.SaveAs("mass3_BW.pdf");
}

