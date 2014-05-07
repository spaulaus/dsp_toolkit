#include <chrono>
#include <fstream>
#include <iostream>
#include <random>

#include <SignalGenerator.hpp>

#include "TraceFilter.hpp"

using namespace std;

int main(int argc, char* argv[]) {
    unsigned int seed = 
        chrono::system_clock::now().time_since_epoch().count();
    mt19937_64 twist (seed);
    uniform_real_distribution<double> mult(0.0,1.0);
    normal_distribution<double> amps(4096, 5.0);

    ofstream output("out.dat");
    
    // Sampling frequency
    double adc = 100;
    // times here in us
    double tl = 0.2, tg = 0.01;
    unsigned int thresh = 6;
    double el = 0.2, eg = 0.01, tau = 0.01;

    //experiment values
    // double tl = 0.2, tg = 0.03;
    // unsigned int thresh = 6;
    // double el = 0.6, eg = 0.24, tau = 0.9;

    double len = 2*(el*adc)+(eg*adc);

    FilterParameters trigger(tl,tg, thresh);
    FilterParameters energy(el,eg,tau);
    TraceFilter filter(adc , trigger, energy);
    //filter.SetVerbose(true);
    
    //in clock tics
    double traceLength = len / (2*el+eg);
    double traceDelay = traceLength*0.5;

    SignalGenerator sig;
    sig.SetSignalType("gaussian");
    //assume the times here are in clockticks
    sig.SetDelay(traceDelay);
    sig.SetSigma(5.0);

    unsigned int numTrials = 1e6;
    for(unsigned int i = 0; i < numTrials; i++) {
        sig.SetAmplitude(amps(twist));
        
        vector<double> single;
        for(double i = 0; i < traceLength; i++)
            single.push_back(sig.GetSignalValue(i));
        
        filter.CalcFilters(&single);
        
        output << sig.GetAmplitude() << " " << filter.GetEnergy() << endl;
    }
    output.close();
}
