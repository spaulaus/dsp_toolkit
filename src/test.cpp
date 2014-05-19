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
    normal_distribution<double> amps(2048, 2);

    ofstream output("out.dat");
    
    // Sampling frequency
    double adc = 100;
    // times here in us
    double tl = 0.2, tg = 0.03;
    unsigned int thresh = 6;
    double el = 0.6, eg = 0.2, tau = 1.;

    //experiment values
    // double tl = 0.2, tg = 0.03;
    // unsigned int thresh = 6;
    // double el = 0.6, eg = 0.24, tau = 0.9;

    double len = 3*(2*(el*adc)+(eg*adc));

    FilterParameters trigger(tl,tg, thresh);
    FilterParameters energy(el,eg,tau);
    TraceFilter filter(adc , trigger, energy);
    //filter.SetVerbose(true);
    
    //in clock tics
    double traceLength = len;
    double traceDelay = len/3;

    SignalGenerator sig;
    sig.SetSignalType("pixie");
    //assume the times here are in clockticks
    sig.SetDelay(traceDelay);
    sig.SetSigma(50.0);
    sig.SetDecayConstant(150.0);
    sig.SetBaseline(0.0);

    unsigned int numTrials = 1e5;
    for(unsigned int i = 0; i < numTrials; i++) {
        sig.SetAmplitude(amps(twist));
        
        vector<double> single;
        for(double i = 0; i < traceLength; i++)
            single.push_back(sig.GetSignalValue(i));
        
        if(i == 0)
            for(const auto &i : single)
                cout << i << endl;
        
        filter.CalcFilters(&single);
        
        output << sig.GetAmplitude() << " " << filter.GetEnergy() << endl;
    }
    output.close();
}
