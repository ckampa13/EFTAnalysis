import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools

if __name__ == '__main__':

    #Bprime histograms
    MW_jj = rt.TH1D("MW_jj", "MW_jj", 500, 0., 500)
    MW_jj.Sumw2()
    MInvariantMass_mumu = rt.TH1F("MInvariantMass_mumu", "MInvariantMass_mumu", 500, 0., 500);
    MInvariantMass_mumu.Sumw2()    
    MInvariantMass_qq = rt.TH1F("MInvariantMass_qq", "MInvariantMass_qq", 500, 0., 1000.0);
    MInvariantMass_qq.Sumw2()
    EW_jj = rt.TH1D("EW_jj", "EW_jj", 500, 0., 1000)
    EW_jj.Sumw2()
    EW_qq = rt.TH1D("EW_qq", "EW_qq", 500, 0., 1000)
    EW_qq.Sumw2()
    pTW_jj = rt.TH1D("pTW_jj", "pTW_jj", 500, 0., 500)
    pTW_jj.Sumw2()
    W1_lv = rt.TLorentzVector()
    W2_lv = rt.TLorentzVector()
    W3_lv = rt.TLorentzVector()
    massW_1 = rt.TH1F("massW_1", "massW_1", 500, 0., 500.0)
    massW_1.Sumw2()
    massW_2 = rt.TH1F("massW_2", "massW_2", 500, 0., 500.0)  
    massW_2.Sumw2()    
    massW_3 = rt.TH1F("massW_3", "massW_3", 500, 0., 500.0)  
    massW_3.Sumw2()
    el_lv =  rt.TLorentzVector()
    nuel_lv =  rt.TLorentzVector()
    h_el_pT =  rt.TH1F("h_el_pT", "h_el_pT", 500, 0., 500.0)
    h_el_pT.Sumw2()
    h_nu_pT =  rt.TH1F("h_nu_pT", "h_nu_pT", 500, 0., 500.0)
    h_nu_pT.Sumw2()
    M_www_sm = rt.TH1D("M_www_sm", "M_www_sm", 500, 0.0, 5000.0)
    M_www_sm.Sumw2()
    M_www_cWm05 = rt.TH1D("M_www_cWm05", "M_www_cWm05", 500, 0.0, 5000.0)
    M_www_cWm05.Sumw2() 
    M_www_cWm5 = rt.TH1D("M_www_cWm5", "M_www_cWm5", 500, 0.0, 5000.0)
    M_www_cWm5.Sumw2()    
    M_www_cWm1 = rt.TH1D("M_www_cWm1", "M_www_cWm1", 500, 0.0, 5000.0)
    M_www_cWm1.Sumw2()  
    M_www_cWp1 = rt.TH1D("M_www_cWp1", "M_www_cWp1", 500, 0.0, 5000.0)
    M_www_cWp1.Sumw2()  
    M_www_cWp5 = rt.TH1D("M_www_cWp5", "M_www_cWp5", 500, 0.0, 5000.0)
    M_www_cWp5.Sumw2() 
    M_www_cWp05 = rt.TH1D("M_www_cWp05", "M_www_cWp05", 500, 0.0, 5000.0)
    M_www_cWp05.Sumw2() 
   

    # find events in file
    myLHEfile = LHEfile(sys.argv[1])
    myLHEfile.setMax(100000)
    #myLHEfile.setMax(2)
    eventsReadIn = myLHEfile.readEvents()
    weightsReadIn = myLHEfile.readWeights()
    sm = []
    cWm05 = []
    cWm5 = []
    cWm1 = []
    cWp5 = []
    cWp1 = []
    cWp05 = []
    for oneWeight in weightsReadIn:
        myLHEevent = LHEevent()
        myLHEevent.fillWeight(oneWeight)
        for i in range(0,len(myLHEevent.Weights)):
            p = myLHEevent.Weights[i]
            if(p['weightID']=='EFT_SM'): sm.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_m05'): cWm05.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_m5'): cWm5.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_m1'): cWm1.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_p5'): cWp5.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_p1'): cWp1.append(p['weightValue'])
            if(p['weightID']=='EFT_cW_p05'): cWp05.append(p['weightValue'])
    #print len(sm)
    eventIdx=0
    for oneEvent in eventsReadIn:
        eventIdx += 1
        #print eventIdx
        #print oneEvent
        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)
        n_mu = 0
        n_q = 0
        n_el = 0
        n_nuel = 0
        mass = []
        for i in range(0,len(myLHEevent.Particles)):
            p = myLHEevent.Particles[i]
            if abs(p['ID'])  == 24: MW_jj.Fill(p['M'])
            if abs(p['ID'])  == 24: EW_jj.Fill(p['E'])
            if (abs(p['ID'])  == 24 and rt.TMath.Sqrt(p['Px']*p['Px'] + p['Py']*p['Py']) > 50.0): pTW_jj.Fill(rt.TMath.Sqrt(p['Px']*p['Px'] + p['Py']*p['Py']))
            if abs(p['ID']) == 24:
                    mass.append(p['M'])
                    mass.sort()
                    if(len(mass)==1): massW_1.Fill(mass[0])
                    if(len(mass)==2): massW_2.Fill(mass[1])
                    if(len(mass)==3): massW_3.Fill(mass[2])
                    if(len(mass)==1): W1_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
                    if(len(mass)==2): W2_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
                    if(len(mass)==3): W3_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
                    if(len(mass)==3): M_www_sm.Fill((W1_lv+W2_lv+W3_lv).M(), sm[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWm05.Fill((W1_lv+W2_lv+W3_lv).M(), cWm05[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWp05.Fill((W1_lv+W2_lv+W3_lv).M(), cWp05[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWm1.Fill((W1_lv+W2_lv+W3_lv).M(), cWm1[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWp1.Fill((W1_lv+W2_lv+W3_lv).M(), cWp1[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWm5.Fill((W1_lv+W2_lv+W3_lv).M(), cWm5[eventIdx-1]/sm[eventIdx-1])
                    if(len(mass)==3): M_www_cWp5.Fill((W1_lv+W2_lv+W3_lv).M(), cWp5[eventIdx-1]/sm[eventIdx-1])
        #print eventIdx
        #print sm[eventIdx-1] 
        print cWp5[eventIdx-1]
        del oneEvent, myLHEevent
        
    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    MW_jj.Write()
    EW_jj.Write()
    MInvariantMass_mumu.Write();
    MInvariantMass_qq.Write();
    pTW_jj.Write()
    massW_1.Write()
    massW_2.Write()
    massW_3.Write()
    M_www_sm.Write()
    M_www_cWm05.Write()
    M_www_cWp05.Write()
    M_www_cWm1.Write()
    M_www_cWp1.Write()
    M_www_cWm5.Write()
    M_www_cWp5.Write()
    histoFILE.Close()
