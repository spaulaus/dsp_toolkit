//******************************************************************************
// Driver to generate the pile-up response of the Pixie module from a
// gaussian distrubution
//
// First load the macro with the model functions: .L pileUpModels.C
// Then load the macro with the pile-up generator: .L pileUpGenerator.C
// Then run this macro: .x PileUpDrivGauss.C
//******************************************************************************

Int_t nGoodShots = 1000000;
Double_t rate = 4.16e4;                         // Rate in cps. (see logbook p.131)

// Properties of the Gaussian distribution
Double_t x0 = 100.;
Double_t sig = 1.;

//******************************************************************************
Double_t Gaussian(Double_t* x, Double_t* par) {
    Double_t xc, s;
    xc = x[0];

    s = exp(-(xc - x0) * (xc - x0) / (2. * sig * sig));
    return (s);
}

//******************************************************************************
void PileUpDrivGauss(void) {
    Double_t xMIN = x0 - 3. * sig, xMAX = x0 + 3. * sig;

// Define generating function
    TF1* fGenFct = new TF1("fGenFctN", Gaussian, xMIN, xMAX, 0);

// Define histograms
    Int_t nCHAN = 512;
    Double_t cMIN = 0., cMAX = 512.;
    hsrc = new TH1F("Source", "source", nCHAN, cMIN, cMAX);
    hpup = new TH1F("PileUp", "pile_up", nCHAN, cMIN, cMAX);
    htot = new TH1F("Total", "total", nCHAN, cMIN, cMAX);
    hexp = new TH1F("hExpN", "hExpT", nCHAN, cMIN, cMAX);
    hexp->FillRandom("fGenFctN", nGoodShots);

    Double_t yMIN = 0., yMAX = hexp->GetMaximum() * 1.01;

    pileUpGenerator(nGoodShots, xMIN, xMAX, yMIN, yMAX, rate);

// Plot spectra
    gStyle->SetOptStat(0);

    TCanvas* c1 = new TCanvas("c1", "Results-1", 100, 100, 700, 500);
    c1->Clear();
    c1->Divide(2, 2);
    c1->cd(1)->SetLogy();
    hsrc->GetXaxis()->SetRangeUser(0., 300.);
    hsrc->Draw();
    c1->cd(2)->SetLogy();
    hpup->GetXaxis()->SetRangeUser(0., 300.);
    hpup->Draw();
    c1->cd(3)->SetLogy();
    htot->GetXaxis()->SetRangeUser(0., 300.);
    htot->Draw();
    c1->Update();

}
//******************************************************************************
