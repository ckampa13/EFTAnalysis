void loopdir() {
    TFile *f1 = TFile::Open("hsimple.root");
    TIter keyList(f1->GetListOfKeys());
    TKey *key;
    int nhist = 0;
    while ((key=(TKey*)keyList())) {
        nhist++;
        TClass *cl = gROOT->GetClass(key->GetClassName());
        if (!cl->InheritsFrom("TH1")) continue;
        TH1 *h = (TH1*)key->ReadObj();\
        cout << "Key #" << nhist << endl;
        cout << "'key'="<< key << endl;
        cout << "Name (key) " << key->GetName() << endl;
        cout << "Name (TH1) " << h->GetName() << endl;
    }
}
