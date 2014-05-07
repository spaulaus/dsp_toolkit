#include <chrono>
#include <fstream>
#include <iostream>
#include <random>

#include <SignalGenerator.hpp>

#include "EnergyFilter.hpp"

using namespace std;

vector<double> TrapFilter(const double &L, const double &G, 
                          const vector<double> &sig);

int main(int argc, char* argv[]) {
    unsigned int seed = 
        chrono::system_clock::now().time_since_epoch().count();
    mt19937_64 twist (seed);
    uniform_real_distribution<double> mult(0.0,1.0);
    lognormal_distribution<double> amps(4096, 5.0);

    ofstream output("out.dat");
    
    //time here in clockticks (energy filter)
    double adc = 100;
    double L = 0.2*adc, G = 0.01*adc, tau = 0.01*adc;
    double len = 2*L+G;

    EnergyFilter filter(L, G, tau);
    
    //in clock tics
    double traceLength = len*2;
    double traceDelay = traceLength*0.25;

    SignalGenerator sig;
    sig.SetSignalType("gaussian");
    //assume the times here are in clockticks
    sig.SetDelay(traceDelay);
    sig.SetSigma(2.0);

    for(unsigned int i = 0; i < 1e6; i++) {
        sig.SetAmplitude(amps(twist));
        
        vector<double> single;
        for(double i = 0; i < traceLength; i++)
            single.push_back(sig.GetSignalValue(i));
        
        double filt = filter.CalcFilter(&single);
        
        output << sig.GetAmplitude() << " " << filt << endl;
    }
    output.close();
}
