#include <chrono>
#include <iostream>
#include <random>

#include <SignalGenerator.hpp>

#include "TrapezoidalFilter.hpp"

using namespace std;

vector<double> TrapFilter(const double &L, const double &G, 
                          const vector<double> &sig);

int main(int argc, char* argv[]) {
    unsigned int seed = 
        chrono::system_clock::now().time_since_epoch().count();
    default_random_engine generator (seed);
    
    //time here in clockticks
    double L = 0.001*100, G = 0.005*100;
    //double L = 0.6*100, G = 0.24*100;
    
    TrapezoidalFilter filter(L, G);
    
    //in clock tics
    double traceLength = 1*100;
    double traceDelay = traceLength*0.25;

    SignalGenerator sig;
    double sigma = 2.0;
    double amplitude = 2.2;
    sig.SetSignalType("gaussian");
    //assume the times here are in us
    sig.SetDelay(traceDelay);
    sig.SetSigma(sigma);
    sig.SetAmplitude(amplitude);
    
    vector<double> single;
    for(double i = 0; i < traceLength; i++)
        single.push_back(sig.GetSignalValue(i));

    vector<double> filt = filter.CalcFilter(&single);

    for(unsigned int i = 0; i < filt.size(); i++)
        cout << i << " " << single.at(i) << " " 
             << filt.at(i) << endl;
}
