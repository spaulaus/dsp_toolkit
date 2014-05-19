/***************************************************************************
  *  Copyright S. V. Paulauskas 2014                                       *
  *                                                                        *
  *  This program is free software: you can redistribute it and/or modify  *
  *  it under the terms of the GNU General Public License as published by  *
  *  the Free Software Foundation, version 3.0 License.                    *
  *                                                                        *
  *  This program is distributed in the hope that it will be useful,       *
  *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
  *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
  *  GNU General Public License for more details.                          *
  *                                                                        *
  *  You should have received a copy of the GNU General Public License     *
  *  along with this program.  If not, see <http://www.gnu.org/licenses/>. *
  **************************************************************************
*/

/** \file test.cpp
 *  \brief A test code to test the filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 *
 *  This code is based off of the IGOR macro energy.ipf
 *  written by H. Tan of XIA LLC and parts of the nscope
 *  program written at the NSCL written by C.Prokop.
 *
 */
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
