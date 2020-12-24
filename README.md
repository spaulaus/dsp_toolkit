# Digital Signal Processing Toolkit

This code started as a C++ program to perform trapezoidal filtering to a digitized signal from
[XIA LLC's Pixie-16 hardware](https://www.xia.com/dgf_pixie-16.html). The original sample code came
from a VB program using [IGOR](https://www.wavemetrics.com/) as its base. It fairly well
approximates the filter calculations that happen on a Pixie-16 module. These algorithms are mostly
focused around XIA's hardware and function, but can be applied to **any** digitized signal.

## Installation
`pip install dsp_toolkit`

## Module Descriptions

### filtering
Implements a simple trapezoidal filter without any bells and whistles. We also include a simple 
RC low-pass filter used for conditioning signals.  

XIA LLC uses [trapezoidal filtering](https://doi.org/10.1109/NSSMIC.2008.4774600) to calculate
trigger positions and energies. The functions in this script approximate the Pixie-16 on-board
calculations. We have functions to calculate

* trigger positions,
* signal baseline,
* signal energy,
* energy sums,
* and trigger and energy responses.

We've made no attempt to convert bins to time. Users can do this trivially if they know the sampling
frequency of their signal.

### sample_data
The sample data include both energy spectra, and digitized signals. The signals can be used with the
various filtering and fitting functions. The energy spectra can be used with pileup calculations. 

### signal_pileup
Takes a user provided energy distribution (either binned or raw) and calculates signal pileups
based on trapezoidal filter parameters and count rates. We've also provided some macros that can be 
used with the CERN ROOT program. Those scripts served as the basis for the python functions. 

### timing
Provides both fitting and constant fraction discrimination (CFD) functions. We implement both a 
traditional CFD, and a CFD described in XIA's Pixie-16 Manual. We implement a couple of different 
fitting functions. The `vandle` function is the most tested and used function.
 
