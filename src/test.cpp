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

    ifstream infile("data/trc.dat");
    if(!infile)
        cerr << "Cannot open input file. Try again, son." << endl;
    else {
        while(infile) {
            if (isdigit(infile.peek())) {
                int junk, junk1;
                infile >> junk >> junk1;
                trc.push_back(junk1);
            } else
                infile.ignore(1000,'\n');
        }
    }
    infile.close();

    //times in us, sampling in MHz, and thresh in ADC units
    unsigned int adc = 100; // in MHz
    double tl = 0.2, tg = 0.03;
    unsigned int thresh = 6;
    double el = 0.6, eg = 0.24, tau = 0.9;

    FilterParameters trigger(tl,tg, thresh);
    FilterParameters energy(el,eg,tau);
    TraceFilter filter(adc , trigger, energy);
    filter.SetVerbose(true);
   
    //Calculate for the original trace
    filter.CalcFilters(&trc);
    double trcEn = filter.GetEnergy();
    cout << "Trace Enegy: " << trcEn << endl;
}
