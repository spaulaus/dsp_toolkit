/** \file TrapezoidalFilter.cpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 */
#include <iostream>

#include "TrapezoidalFilter.hpp"

using namespace std;

TrapezoidalFilter::TrapezoidalFilter(const double &len, const double &ftop) {
    g_ = ftop;
    l_ = len;
}

vector<double> TrapezoidalFilter::CalcFilter(const vector<double> *sig) {
    vector<double> filter;
    for(unsigned int k = 0; k < sig->size(); k++) {
        double partA = 0, partB = 0;

        // cout << k-2*l_-g_+1 << " " << k-l_-g_ << " " 
        //      << k-l_+1 << " " << k << endl;
                
        for(unsigned int i = k-2*l_-g_+1; i < k-l_-g_; i++)
            partA += sig->at(i);
        for(unsigned int i = k-l_+1; i < k; i++)
            partB += sig->at(i);
        filter.push_back((-partA+partB)/l_);
    }
    return(filter);
}
