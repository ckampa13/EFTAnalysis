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

  double numberOfevents = 100000.0;
  double lumi = 137.0;
  double onshell_crosssection = 0.009649*1000.0*0.68666533;//0.010663964*1000.0*0.68666533;//0.007969*1000.0*0.68666533;//0.010663964*1000.0;
  //double onshell_crosssection = 0.012605527586*1000.0; 
  //double onshell_crosssection = 0.009649*1000.0; 
  double offshell_crosssection = 0.009649*1000.0;
  double onshell_crosssection_vh =  0.002881*1000.0*1.25;//0.001618*1000.0;//0.002881*1000.0; 

/*  TFile* fileWWW_BW15 = new TFile("test_sapta_15.root");
  TH1F *hWWW_BW15 = (TH1F*)fileWWW_BW15->Get("M_elnu");
  hWWW_BW15->SetTitle("");
  hWWW_BW15->SetLineColor(kBlack);
  hWWW_BW15->SetLineWidth(2);
  hWWW_BW15->Rebin(50);
  hWWW_BW15->GetXaxis()->SetRangeUser(0.0, 750.0);
  hWWW_BW15->SetFillColor(kBlack);
  hWWW_BW15->SetFillStyle(3004);
  hWWW_BW15->SetMinimum(0.001);
  hWWW_BW15->SetStats(kFALSE);
  hWWW_BW15->Scale(offshell_crosssection*lumi/numberOfevents);
  hWWW_BW15->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW15->GetXaxis()->SetTitleOffset(1.3);
  hWWW_BW15->GetXaxis()->SetTitle("#splitline{Mass of the W boson}{(electron + neutrino invariant mass) [GeV]}");
  hWWW_BW15->GetYaxis()->SetTitle("Events");
  hWWW_BW15->SetMinimum(0.001);
  hWWW_BW15->Draw("HIST");

  TFile* fileWWW_BW100000 = new TFile("test_WWWOnshell_bw15.root");
  TH1F *hWWW_BW100000 = (TH1F*)fileWWW_BW100000->Get("M_elnu");
  hWWW_BW100000->SetLineColor(kGreen+3);
  hWWW_BW100000->SetLineWidth(2);
  hWWW_BW100000->SetFillColor(kGreen+3);
  hWWW_BW100000->SetFillStyle(3005); 
  hWWW_BW100000->Rebin(50);
  hWWW_BW100000->GetXaxis()->SetRangeUser(0.0, 750.0);
  hWWW_BW100000->SetStats(kFALSE);
  hWWW_BW100000->Scale(onshell_crosssection*lumi/numberOfevents);
  hWWW_BW100000->GetYaxis()->SetTitleOffset(1.3);
  hWWW_BW100000->Draw("HIST SAME");

  TFile* fileVH_BW100000 = new TFile("test_Feb24.root");
  TH1F *hVH_BW100000 = (TH1F*)fileVH_BW100000->Get("M_elnu");
  hVH_BW100000->SetFillColor(kBlue);
  hVH_BW100000->SetFillStyle(3004);  
  hVH_BW100000->SetLineColor(kBlue);
  hVH_BW100000->SetLineWidth(2);
  hVH_BW100000->Rebin(50);
  hVH_BW100000->GetXaxis()->SetRangeUser(0.0, 750.0);
  hVH_BW100000->SetStats(kFALSE);
  hVH_BW100000->Scale(onshell_crosssection_vh*lumi/numberOfevents);
  hVH_BW100000->GetYaxis()->SetTitleOffset(1.3);
  hVH_BW100000->Draw("HIST SAME");
*/
  TFile* fileNP_BW100000 = new TFile("test_unweighted_events_FT0.root");
  TH1F *hNP_BW100000 = (TH1F*)fileNP_BW100000->Get("M_elnu");
  hNP_BW100000->SetFillColor(kMagenta);
  hNP_BW100000->SetFillStyle(3005);
  hNP_BW100000->SetLineColor(kMagenta);
  hNP_BW100000->SetLineWidth(2);
  hNP_BW100000->Rebin(50);
  hNP_BW100000->GetXaxis()->SetRangeUser(0.0, 750.0);
  hNP_BW100000->SetStats(kFALSE);
  hNP_BW100000->GetYaxis()->SetTitleOffset(1.3);
  hNP_BW100000->GetXaxis()->SetTitleOffset(1.3);
  hNP_BW100000->GetXaxis()->SetTitle("#splitline{Mass of the W boson}{(electron + neutrino invariant mass) [GeV]}");
  hNP_BW100000->GetYaxis()->SetTitle("Events");
  hNP_BW100000->Scale(onshell_crosssection*lumi/numberOfevents);
  hNP_BW100000->GetYaxis()->SetTitleOffset(1.3);
  hNP_BW100000->Draw("HIST");

  TFile* fileNP_1_BW100000 = new TFile("test_unweighted_events_FT0_1.root");
  TH1F *hNP_1_BW100000 = (TH1F*)fileNP_1_BW100000->Get("M_elnu");
  hNP_1_BW100000->SetFillColor(kBlue);
  hNP_1_BW100000->SetFillStyle(3004);
  hNP_1_BW100000->SetLineColor(kBlue);
  hNP_1_BW100000->SetLineWidth(2);
  hNP_1_BW100000->Rebin(50);
  hNP_1_BW100000->GetXaxis()->SetRangeUser(0.0, 750.0);
  hNP_1_BW100000->SetStats(kFALSE);
  hNP_1_BW100000->Scale(onshell_crosssection*lumi/numberOfevents);
  hNP_1_BW100000->GetYaxis()->SetTitleOffset(1.3);
  hNP_1_BW100000->Draw("HIST SAME");

  TLegend *leg1 = new TLegend(0.45,0.55,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
// leg1->AddEntry(hWWW_BW15,"With offshell contribution","f");
//  leg1->AddEntry(hWWW_BW100000,"Onshell BW cutoff: 15#sigma", "f");
//  leg1->AddEntry(hVH_BW100000,"Higgs (VH)", "f");
  leg1->AddEntry(hNP_BW100000,"New Physics (FT0)", "f");
  leg1->AddEntry(hNP_1_BW100000,"New Physics (FT0) realistic", "f"); 
  leg1->Draw();

  c1.SaveAs("mass_elnu_BW_simpleComparison_NP.png");
  c1.SaveAs("mass_elnu_BW_simpleComparison_NP.pdf");
}

