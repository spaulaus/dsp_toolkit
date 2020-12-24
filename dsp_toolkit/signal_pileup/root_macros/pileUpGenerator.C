//******************************************************************************
// Generates a pile-up spectrum from a pdf given by histogram hexp
// This macro has to be loaded before running any driver.
// The macro with the model functions has to be loaded first: .L pileUpModels.C
//******************************************************************************

TRandom3 u;

// Declare histograms
TH1F* hexp;
TH1F* hsrc;
TH1F* hpup;
TH1F* htot;

//******************************************************************************
Double_t pdf(Double_t x) {
    Double_t s;

    s = hexp->GetBinContent(x);
    return (s);
}

//******************************************************************************
void pileUpGenerator(Int_t nShots, Double_t XMIN, Double_t XMAX, Double_t YMIN, Double_t YMAX, Double_t RATE) {
    Double_t x1, y1, x2, y2;
    Double_t P, T, pUpEnergy;

    fprintf(stderr, "Starting pile up generator...");
    Int_t nevents = nShots;
    while (nevents > 0) {
        // First shot in the energy distribution
        x1 = (XMAX + XMIN) / 2.;
        y1 = YMAX;
        while (y1 > pdf(x1)) {
            x1 = XMIN + (XMAX - XMIN) * u.Rndm();
            y1 = YMIN + (YMAX - YMIN) * u.Rndm();
        }
        hsrc->Fill(x1);

        // Second shot in the energy distribution
        x2 = (XMAX + XMIN) / 2.;
        y2 = YMAX;
        while (y2 > pdf(x2)) {
            x2 = XMIN + (XMAX - XMIN) * u.Rndm();
            y2 = YMIN + (YMAX - YMIN) * u.Rndm();
        }
        hsrc->Fill(x2);

        // Generate a time interval following Possion distribution
        P = u.Rndm();
        T = -log(1. - P) / RATE;

        // Now test the pile-up and fill histograms
        if (T <= tPU) {
            pUpEnergy = getPileUpEnergy(T, x1, x2);
            hpup->Fill(pUpEnergy);
            htot->Fill(pUpEnergy);
            nevents--;
        } else if (T > tPU)                // No pile-up
        {
            htot->Fill(x1);
            htot->Fill(x2);
            nevents -= 2;
        }

    }// end of while loop over events


    fprintf(stderr, "done\n");
}
//******************************************************************************
