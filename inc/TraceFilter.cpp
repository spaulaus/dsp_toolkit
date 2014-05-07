/** \file EnergyFilter.hpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 */
#ifndef __ENERGYFILTER_HPP__
#define __ENERGYFILTER_HPP__
#include <vector>

class EnergyFilter {
public:
    EnergyFilter(){};
    EnergyFilter(const double &len, const double &ftop, const double &tau);
    ~EnergyFilter(){};

    double GetFlattop(void){return(g_);};
    double GetRisetime(void){return(l_);};
    double GetTau(void){return(tau_);};

    double CalcFilter(const std::vector<double> *sig);

    void SetFlattop(const double &a){g_ = a;};
    void SetRisetime(const double &a){l_ = a;};
    void SetTau(const double &a){tau_ = a;};
    void SetSig(const std::vector<double> *sig){sig_ = sig;};
private:
    double g_, l_, tau_;
    const std::vector<double> *sig_;
    std::vector<double> coeffs_;
    std::vector<unsigned int> limits_;

    void CalcFilterLimits(const unsigned int &size);
    void CalcFilterCoeffs(void);
};

#endif //__ENERGYFILTER_HPP__
