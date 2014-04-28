/** \file TrapezoidalFilter.hpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 */
#ifndef __TRAPEZOIDALFILTER_HPP__
#define __TRAPEZOIDALFILTER_HPP__
#include <vector>

class TrapezoidalFilter {
public:
    TrapezoidalFilter(){};
    TrapezoidalFilter(const double &len, const double &ftop);
    ~TrapezoidalFilter(){};

    double GetFlattop(void){return(g_);};
    double GetRisetime(void){return(l_);};

    std::vector<double> CalcFilter(const std::vector<double> *sig);

    void SetFlattop(const double &a){g_ = a;};
    void SetRisetime(const double &a){l_ = a;};
private:
    double g_, l_; 
    std::vector<double> filt_;
};

#endif //__TRAPEZOIDALFILTER_HPP__
