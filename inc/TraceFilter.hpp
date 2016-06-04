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
/** \file TraceFilter.hpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 *
 *  This code is based off of the IGOR macro energy.ipf
 *  written by H. Tan of XIA LLC and parts of the nscope
 *  program written at the NSCL written by C.Prokop.
 *
 */
#ifndef __TRACEFILTER_HPP__
#define __TRACEFILTER_HPP__
#include <vector>
#include <utility>

#include "TrapFilterParameters.hpp"

/*! The class to perform the filtering */
class TraceFilter {
public:
    /** Default Constructor */
    TraceFilter(){};
    /** Constructor 
     * \param [in] nsPerSample : The ns/Sample for the ADC */
    TraceFilter(const int &nsPerSample){nsPerSample_ = nsPerSample;}
    /** Constructor 
     * \param [in] nsPerSample : The ns/Sample for the ADC 
     * \param [in] tFilt : Parameters for the trigger filter
     * \param [in] eFilt : Paramters for the energy filter
     * \param [in] analyzePileup : True if we want additional analysis for pileups. */
    TraceFilter(const unsigned int &nsPerSample, 
                const TrapFilterParameters &tFilt,
                const TrapFilterParameters &eFilt,
                const bool &analyzePileup = false);
    /** Default Destructor */
    ~TraceFilter(){}
    
    bool GetHasPileup(void){return(trigs_.size() > 1);}
    
    double GetNsPerSample(void){return(nsPerSample_);}
    double GetBaseline(void){return(baseline_);}
    double GetEnergy(void){return(energy_);}

    unsigned int GetNumTriggers(void) {return(trigs_.size());}
    unsigned int GetTrigger(void){return(trigs_[0]);}
    
    std::vector<double> GetTriggerFilter(void) {return(trigFilter_);}
    std::vector<double> GetEnergyFilterCoefficients(void) {return(coeffs_);}
    std::vector<double> GetEnergySums(void) {return(esums_);}

    std::vector<unsigned int> GetTriggers(void){return(trigs_);}
    std::vector<unsigned int> GetEnergySumLimits(void){return(limits_);}

    void CalcFilters(const std::vector<double> *sig);
    void SetAdcSample(const double &a){nsPerSample_ = a;}
    void SetEnergyParams(const TrapFilterParameters &a) {e_ = a; ConvertToClockticks();}
    void SetSig(const std::vector<double> *sig){sig_ = sig;}
    void SetTriggerParams(const TrapFilterParameters &a) {t_ = a; ConvertToClockticks();}
    void SetVerbose(const bool &a){isVerbose_ = a;}

private:
    bool isVerbose_;
    bool isConverted_;
    bool analyzePileup_;

    double baseline_;
    double energy_;

    unsigned int nsPerSample_;

    TrapFilterParameters e_;
    TrapFilterParameters t_;
    
    const std::vector<double> *sig_;
    std::vector<double> coeffs_;
    std::vector<double> trigFilter_;
    std::vector<double> esums_;
    
    std::vector<unsigned int> limits_;
    std::vector<unsigned int> trigs_;
    
    void CalcBaseline(void); 
    void CalcEnergyFilterLimits(void);
    void CalcTriggerFilter(void);

    void CalcEnergyFilterCoeffs(void);
    void CalcEnergyFilter(void);
    void CheckIfPileup(void);
    void ConvertToClockticks(void);
    void Reset(void);

    enum ErrTypes{NO_TRIG,LATE_TRIG,BAD_FILTER_COEFF,BAD_FILTER_LIMITS,EARLY_TRIG};
};
#endif //__TRACEFILTER_HPP__
