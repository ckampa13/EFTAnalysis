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

  TFile* fileWWW_Onshell_BW15 = new TFile("test_Onshell_15.root");
  TH1F *hWWW_Onshell_BW15 = (TH1F*)fileWWW_Onshell_BW15->Get("M_elnu");
  hWWW_Onshell_BW15->SetLineColor(kMagenta);
  hWWW_Onshell_BW15->SetLineWidth(2);
  hWWW_Onshell_BW15->Rebin(20);
  hWWW_Onshell_BW15->GetXaxis()->SetRangeUser(0.0, 200.0);
  hWWW_Onshell_BW15->SetStats(kFALSE);
  hWWW_Onshell_BW15->SetTitle("");
  hWWW_Onshell_BW15->GetYaxis()->SetTitleOffset(1.3);
  hWWW_Onshell_BW15->GetXaxis()->SetTitleOffset(1.3);
  hWWW_Onshell_BW15->GetXaxis()->SetTitle("#splitline{Mass of the W boson}{(electron + neutrino invariant mass) [GeV]}");
  hWWW_Onshell_BW15->GetYaxis()->SetTitle("Events");
  hWWW_Onshell_BW15->Draw("HIST");

  TLegend *leg1 = new TLegend(0.52,0.55,0.80,0.82,NULL,"brNDC");
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.03);
  leg1->SetLineColor(1);
  leg1->SetLineStyle(0);
  leg1->SetLineWidth(1);
  leg1->SetFillColor(10);
  leg1->SetFillStyle(0);
  leg1->AddEntry(hWWW_Onshell_BW15,"Onshell BW cutoff: 15","l");
  leg1->Draw();

  c1.SaveAs("mass_elnu_BW_Onshell.png");
  c1.SaveAs("mass_elnu_BW_Onshell.pdf");
}

