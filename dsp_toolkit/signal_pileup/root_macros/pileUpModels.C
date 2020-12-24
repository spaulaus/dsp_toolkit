//******************************************************************************
// Define functions for models describing the response of Pixie16 modules
// to pile-up.
// The functions are called by the pileup drivers.
//******************************************************************************

// Define time constants
/***
Double_t tRISE = 0.08e-6;                       // CsI(Na) signal Rise time in s.
Double_t tGAP = 0.24e-6;                        // GAP time (G) in s.
Double_t tPEAK = 0.60e-6;                       // Peaking time (L) in s.
***/

/***
Double_t tRISE = 0.08e-6;                       // CsI(Na) signal Rise time in s.
Double_t tGAP = 0.60e-6;                        // GAP time (G) in s.
Double_t tPEAK = 0.24e-6;                       // Peaking time (L) in s.
***/


/***
Double_t tRISE = 0.08e-6;                       // CsI(Na) signal Rise time in s.
Double_t tGAP = 0.68e-6;                        // GAP time (G) in s.
Double_t tPEAK = 0.16e-6;                       // Peaking time (L) in s.
***/


// Parameters for Model 4
Double_t tRISE = 0.10e-6;                       // CsI(Na) signal Rise time in s.
Double_t tDECAY = 0.76e-6;                      // CsI(Na) signal Decay time in s.
/***
Double_t tGAP = 0.24e-6;                        // GAP time (G) in s.
Double_t tPEAK = 0.60e-6;                       // Peaking time (L) in s.
Double_t tTAU = 0.9e-6;                         // Filter Decay time in s.
***/
Double_t tGAP = 0.64e-6;                        // GAP time (G) in s.
Double_t tPEAK = 0.20e-6;                       // Peaking time (L) in s.
Double_t tTAU = 0.86e-6;                        // Filter Decay time in s.

Double_t tSPL = 10.e-9;                         // Sampling time (for 100 MHz modules)
Double_t SL = tPEAK/tSPL;
Double_t b = exp(-tSPL/tTAU);
Double_t C0 = -(1-b)*pow(b,SL)/(1.-pow(b,SL));
Double_t Cg = 1.-b;
Double_t C1 = (1.-b)/(1.-pow(b,SL));

Double_t tPU = tGAP+tPEAK;
Double_t NSTP = 50.;                            // Samplings in the integration window
Double_t tSTP = tPU/NSTP;


//******************************************************************************
Double_t decayFct(Double_t t) {
    Double_t s;
//s = 1.;
    s = exp(-(t - tRISE) / tDECAY);

    return (s);
}

//******************************************************************************
Double_t signalFct(Double_t t) {
    Double_t f0, f1, f2;
    f0 = 0.;
    f1 = t / tRISE;
    f2 = decayFct(t);

    if (t < 0.)
        return (f0);

    else if ((0. <= t) && (t < tRISE))
        return (f1);

    else if (tRISE <= t)
        return (f2);

    return (0.);
}

//******************************************************************************
Double_t getPileUpEnergy(Double_t dT, Double_t x1, Double_t x2) {
    Double_t pUpEnergy;

//**************** Model 1: rectangular pulses
/***
if(dT <= tGAP)
  {
  pUpEnergy = x1 + x2;
  }
else if( (tGAP < dT)&&(dT <= tPU) )
       {
       pUpEnergy = x1 + x2*( 1. - (dT-tGAP)/(tPU-tGAP) );
       }
***/
// End of Model 1



//**************** Model 2: Trapezoidal pulses, geometrical integration
/***
Double_t A2,A,B,b,X,Y,X1,X2;
if( (dT <= tGAP-tRISE) )                                // Second pulse rises fully inside GAP
  {
  A2 = x2*tPEAK;
  }

else if( (tGAP-tRISE < dT)&&(dT <= tGAP) )              // Second pulse rises between GAP and PEAK
       {
       X = dT+tRISE-tGAP;
       Y = X*x2/tRISE;
       A = X*Y/2.;
       A2 = x2*tPEAK - A;
       }

else if( (tGAP < dT)&&(dT <= tGAP+tPEAK-tRISE) )        // Second pulse rises fully inside PEAK
       {
       B = tPEAK+tGAP-dT;
       b = B-tRISE;
       A2 = (B+b)*x2/2.;
       }

else if( (tGAP+tPEAK-tRISE < dT)&&(dT <= tGAP+tPEAK) )  // Second pulse rises at the end of PEAK
       {
       X = tPEAK+tGAP-dT;
       Y = X*x2/tRISE;
       A2 = X*Y/2.;
       }

X1 = x1;
X2 = A2/tPEAK;
pUpEnergy = X1 + X2;
***/
// End of Model 2


//**************** Model 3: Arbitrary pulse shape, sampling integration
/***
Double_t ampInt=0.,ampNorm=0.;

for(Double_t t=tGAP; t<tPU; t+=tSTP)
   {
   ampInt += x1*signalFct(t) + x2*signalFct(t-dT);
   ampNorm += 1.;
   }
pUpEnergy = ampInt/ampNorm;
***/
// End of Model 3



//**************** Model 4: Use sums with filter parameters, sampling integration
    Double_t S0 = 0., Sg = 0., S1 = 0.;

    for (Double_t t = 0.; t < tGAP; t += tSPL) {
        Sg += x1 * signalFct(t) + x2 * signalFct(t - dT);
    }

    for (Double_t t = tGAP; t < tPU; t += tSPL) {
        S1 += x1 * signalFct(t) + x2 * signalFct(t - dT);
    }

    pUpEnergy = C0 * S0 + Cg * Sg + C1 * S1;
// End of Model 4

    return (pUpEnergy);
}

//******************************************************************************
