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

  TFile* fileWWW_BW15 = new TFile("test_sapta_15.root");
  TH1F *hWWW_BW15 = (TH1F*)fileWWW_BW15->Get("M_elnu");
  hWWW_BW15->SetTitle("");
  hWWW_BW15->SetLineColor(kBlack);
  hWWW_BW15->SetLineWidth(2);
  hWWW_BW15->Rebin(20);
  hWWW_BW15->GetXaxis()->SetRangeUser(0.0, 350.0);
  hWWW_BW15->SetMinimum(0.00001);
  if(hWWW_BW15->Integral() > 0.0) hWWW_BW15->Scale(1.0/hWWW_BW15->Integral());
  hWWW_BW15->SetStats(kFALSE);
  hWWW_BW15->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW15->GetXaxis()->SetTitleOffset(1.3);
  hWWW_BW15->GetXaxis()->SetTitle("#splitline{Mass of the W boson}{(electron + neutrino invariant mass) [GeV]}");
  hWWW_BW15->GetYaxis()->SetTitle("A.U.");
  hWWW_BW15->Draw("HIST");

  TFile* fileWWW_BW10 = new TFile("test_sapta_10.root");
  TH1F *hWWW_BW10 = (TH1F*)fileWWW_BW10->Get("M_elnu");
  hWWW_BW10->SetLineColor(kGreen+3);
  hWWW_BW10->SetLineWidth(2);
  hWWW_BW10->Rebin(20);
  hWWW_BW10->GetXaxis()->SetRangeUser(0.0, 350.0);
  if(hWWW_BW10->Integral() > 0.0) hWWW_BW10->Scale(1.0/hWWW_BW10->Integral());
  hWWW_BW10->SetStats(kFALSE);
  hWWW_BW10->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW10->Draw("HIST SAME");

  TFile* fileWWW_BW5 = new TFile("test_sapta_5.root");
  TH1F *hWWW_BW5 = (TH1F*)fileWWW_BW5->Get("M_elnu");
  hWWW_BW5->SetLineColor(kBlue);
  hWWW_BW5->SetLineWidth(2);
  hWWW_BW5->Rebin(20);
  hWWW_BW5->GetXaxis()->SetRangeUser(0.0, 350.0);
  if(hWWW_BW5->Integral() > 0.0) hWWW_BW5->Scale(1.0/hWWW_BW5->Integral());
  hWWW_BW5->SetStats(kFALSE);
  hWWW_BW5->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW5->Draw("HIST SAME");

  TFile* fileWWW_BW1 = new TFile("test_sapta_1.root");
  TH1F *hWWW_BW1 = (TH1F*)fileWWW_BW1->Get("M_elnu");
  hWWW_BW1->SetLineColor(kRed);
  hWWW_BW1->SetLineWidth(2);
  hWWW_BW1->Rebin(20);
  hWWW_BW1->GetXaxis()->SetRangeUser(0.0, 350.0);
  if(hWWW_BW1->Integral() > 0.0) hWWW_BW1->Scale(1.0/hWWW_BW1->Integral());
  hWWW_BW1->SetStats(kFALSE);
  hWWW_BW1->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW1->Draw("HIST SAME");

  /*TFile* fileWWW_Onshell_BW15 = new TFile("test_WWWOnshell_bw100000.root");
  TH1F *hWWW_Onshell_BW15 = (TH1F*)fileWWW_Onshell_BW15->Get("M_elnu");
  hWWW_Onshell_BW15->SetLineColor(kMagenta);
  hWWW_Onshell_BW15->SetLineWidth(2);
  hWWW_Onshell_BW15->Rebin(20);
  hWWW_Onshell_BW15->GetXaxis()->SetRangeUser(0.0, 350.0);
  hWWW_Onshell_BW15->SetStats(kFALSE);
  hWWW_Onshell_BW15->GetYaxis()->SetTitleOffset(1.3);
  //hWWW_Onshell_BW15->Draw("HIST SAME");
*/
  TLegend *leg1 = new TLegend(0.52,0.55,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->AddEntry(hWWW_BW15,"BW cutoff: 15","l");
  leg1->AddEntry(hWWW_BW10,"BW cutoff: 10","l");
  leg1->AddEntry(hWWW_BW5,"BW cutoff: 5","l");
  leg1->AddEntry(hWWW_BW1,"BW cutoff: 1","l");
  //leg1->AddEntry(hWWW_Onshell_BW15,"Onshell BW cutoff: 25","l");
  leg1->Draw();

  c1.SaveAs("mass_elnu_BW.png");
  c1.SaveAs("mass_elnu_BW.pdf");
}

