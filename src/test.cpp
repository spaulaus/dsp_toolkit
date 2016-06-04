/***************************************************************************
  *  Copyright S. V. Paulauskas 2014-2016                                   *
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
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <random>

#include <SignalGenerator.hpp>

#include "TraceFilter.hpp"

using namespace std;

int main(int argc, char* argv[]) {
    vector<double> trc, trcMb, trcP;
    unsigned int seed = 
        chrono::system_clock::now().time_since_epoch().count();
    mt19937_64 twist (seed);
    uniform_real_distribution<double> mult(0.0,1.0);
    normal_distribution<double> amps(2048, 2);

    ifstream infile("data/piledupTrc.dat");
    if(!infile) {
        cerr << "Cannot open input file. Try again, son." << endl;
        exit(1);
    } else {
        while(infile) {
            if (isdigit(infile.peek())) {
                int junk1;
                infile >> junk1;
                trc.push_back(junk1);
            } else
                infile.ignore(1000,'\n');
        }
    }
    infile.close();

    
    //times in ns, sampling in ns/S, and thresh in ADC units
    unsigned int adc = 10; // in ns/S
    double tl = 100, tg = 30;
    unsigned int thresh = 20;
    double el = 600, eg = 240, tau = 90;
    
    TrapFilterParameters trigger(tl,tg, thresh);
    TrapFilterParameters energy(el,eg,tau);

    double eLen = energy.GetSize() / adc;

    TraceFilter filter(adc , trigger, energy);
    filter.SetVerbose(true);
   
    if(filter.CalcFilters(&trc) != 0)
        exit(0);
    
    vector<double> trig = filter.GetTriggerFilter();
    vector<double> esums = filter.GetEnergySums();
    
    ofstream output("trig.dat");
    if(output)
        for(const auto &i : trig)
            output << i << endl;
    output.close();
    
    //The energy sum information
    double sumL = 20489;
    double sumG = 10040;
    double sumT = 16508;
    //double pE   = 1179;

    double pb = 3780.7283;
    double pbPerSamp = pb / eLen;

    vector<double> coeffs = filter.GetEnergyFilterCoefficients();
    double trcEn = filter.GetEnergy();

    cout << endl << "Calculations using my coefficients" << endl
         << "----------------------------" << endl;
    cout << "Trc Energy Sums : ";
    for(const auto &i : esums)
        cout << i << " ";
    cout << endl;
    
    cout << "Trace Energy: " << trcEn << endl;
    cout << "Esums Energy Calc 1 : " 
         << sumL*coeffs[0]+sumG*coeffs[1]+sumT*coeffs[2]-pbPerSamp
         << endl;
    cout << "Esums Energy Calc 2 : " 
         << (sumL-pbPerSamp)*coeffs[0]+(sumG-pbPerSamp)*coeffs[1]+(sumT-pbPerSamp)*coeffs[2]
         << endl;
    cout << "Esums Energy Calc 3 : " 
         << sumL*coeffs[0]+sumG*coeffs[1]+sumT*coeffs[2]
         << endl;
    cout << "Esums Energy Calc 4 : " 
         << (sumL-pb)*coeffs[0]+(sumG-pb)*coeffs[1]+(sumT-pb)*coeffs[2]
         << endl;
    cout << "Esums Energy Calc 5 : " 
         << (sumL/(el*adc))*coeffs[0]+(sumG/(el*adc))*coeffs[1]+(sumT/(el*adc))*coeffs[2]
         << endl;
    cout << "Esums Energy Calc 6 : " 
         << (sumL/(el*adc))+(sumG/(el*adc))+(sumT/(el*adc))
         << endl;

    double b1 = exp(-1/(tau*adc));
    double a0 = pow(b1,el*adc)/(pow(b1,el*adc)-1.0);
    double ag = 1.0;
    double a1 = -1.0/(pow(b1,el*adc)-1.0);
    cout << endl << "Calculations using C. Prokop's coefficients" << endl
         << "----------------------------" << endl;
    cout << "Coeffs: " << endl << "  a0 = " << a0 << endl << "  ag = " << ag << endl 
         << "  a1 = " << a1 << endl;
    cout << "Esums Energy Calc 1 : " 
         << (sumL)*a0+(sumG)*ag+(sumT)*a1 - pb
         << endl;
    cout << "Esums Energy Calc 2 : " 
         << (sumL-pb)*a0+(sumG-pb)*ag+(sumT-pb)*a1
         << endl;
}
