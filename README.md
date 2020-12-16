# Digital Signal Processing Toolbox
This code started as a C++ program to perform trapezoidal filtering to a digitized signal from 
[XIA LLC's Pixie-16 hardware](https://www.xia.com/dgf_pixie-16.html). The original sample code came
from a VB program using [IGOR](https://www.wavemetrics.com/) as its base. It fairly well approximates 
the filter calculations that happen on a Pixie-16 module. These algorithms are mostly focused around 
XIA's hardware and function, but can be applied to **any** digitized signal. 

## Module Descriptions
## filtering
### trapezoidal_filters.py
XIA LLC uses [trapezoidal filtering](https://doi.org/10.1109/NSSMIC.2008.4774600) to calculate 
trigger positions and energies. The functions in this script approximate the Pixie-16 on-board 
calculations. We have functions to calculate
* trigger positions,
* signal baseline,
* signal energy,
* and trigger and energy responses.
 
We've made no attempt to convert bins to time. Users can do this trivially if they know the sampling
frequency of their signal. 

## sample_data
### sample_traces.py
This script contains sample signals that users can use to explore the performance of the code. See 
the in code documentation for more information about the signals. 

## Installation
As of right now the programs don't have any special dependencies. Just download and run. 
