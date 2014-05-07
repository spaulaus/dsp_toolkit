/** \file EnergyFilter.cpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 *
 *  This code is based off of the IGOR macro energy.ipf
 *  written by H. Tan of XIA LLC. 
 */
#include <iostream>

#include <cmath>

#include "EnergyFilter.hpp"

using namespace std;

EnergyFilter::EnergyFilter(const double &len, const double &ftop, const double &tau) {
    //time here in clockticks
    g_ = ftop;
    l_ = len;
    tau_ = tau;
}

double EnergyFilter::CalcFilter(const vector<double> *sig) {
    sig_ = sig;
    CalcFilterLimits(sig->size());
    CalcFilterCoeffs();
    
    double partA = 0, partB = 0, partC = 0;

    for(unsigned int i = limits_[0]; i < limits_[1]; i++)
        partA += sig->at(i);
    for(unsigned int i = limits_[2]; i < limits_[3]; i++)
        partB += sig->at(i);
    for(unsigned int i = limits_[4]; i < limits_[5]; i++)
        partC += sig->at(i);

    return(coeffs_[0]*partA + coeffs_[1]*partB + coeffs_[2]*partC);
}

void EnergyFilter::CalcFilterCoeffs(void) {
    double beta = exp(-1.0/tau_);
    double c0 = 1-beta;
    double c1 = 1-pow(beta,l_);
    coeffs_.push_back(-(c0/c1)*pow(beta,l_));
    coeffs_.push_back(c0);
    coeffs_.push_back(c0/c1);

    //cout << coeffs_[0] << " " << coeffs_[1] << " " << coeffs_[2] << endl;
}

void EnergyFilter::CalcFilterLimits(const unsigned int &size) {
    double p0 = 0;
    double p1 = p0+l_-1;
    double p2 = p0+l_;
    double p3 = p0+l_+g_-1;
    double p4 = p0+l_+g_;
    double p5 = p0+2*l_+g_-1;
    
    if(p5 > size)
        p5 = (double)size;

    // cout << p0 << " " << p1 << " " << p2 << " "
    //      << p3 << " " << p4 << " " << p5 << " " 
    //      << size << endl;

    limits_.push_back(p0);		// beginning of  sum E0
    limits_.push_back(p1);		// end of sum E0
    limits_.push_back(p2);		// beginning of gap sum
    limits_.push_back(p3);		// end of gap sum
    limits_.push_back(p4);		// beginning of sum E1
    limits_.push_back(p5);		// end of sum E1
}

