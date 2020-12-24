# Digital Signal Processing Toolkit

This code started as a C++ program to perform trapezoidal filtering to a digitized signal from
[XIA LLC's Pixie-16 hardware](https://www.xia.com/dgf_pixie-16.html). The original sample code came
from a VB program using [IGOR](https://www.wavemetrics.com/) as its base. It fairly well
approximates the filter calculations that happen on a Pixie-16 module. These algorithms are mostly
focused around XIA's hardware and function, but can be applied to **any** digitized signal.

## Installation

`pip install dsp-toolkit`

### Verify installation

You can verify the installation by opening up a python console and executing the following

```python
from dsp_toolkit.sample_data import sample_traces as st
import dsp_toolkit.filtering.filters as ft

filter = ft.calculate_trapezoidal_filter(st.plastic_scintillator, 10, 5)
print(filter)
```

Your results should be identical to

```python
results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6, 0.4, 0.5,
           0.2, 0.6, 0.7, 0.3, 0.0, 0.0, 0.0, -0.1, -0.3, -0.1, -0.1, -0.1, 0.1, 0.0, -0.1, 0.3,
           0.3, 0.2, 0.0, -0.3, -0.1, 0.0, 0.0, 0.1, -0.1, -0.2, 0.2, 0.2, 0.0, -0.2, -0.2, 0.0,
           0.1, 0.0, 0.0, -0.2, 0.4, 0.9, 0.8, 0.7, 0.6, 0.5, 0.7, 0.8, 0.6, 6.5, 74.8, 267.0,
           574.5, 912.4, 1215.2, 1463.4, 1657.5, 1805.4, 1909.0, 1921.7, 1789.9, 1526.5, 1220.0,
           940.1, 703.5, 456.4, 129.2, -278.9, -695.9, -1063.5, -1359.4, -1583.3, -1749.9, -1866.3,
           -1888.6, -1764.0, -1505.7, -1198.9, -912.5, -676.4, -497.0, -363.7, -266.1, -191.3,
           -130.7, -85.5, -56.4, -38.8, -28.2, -21.0, -15.7, -10.8, -10.3, -16.8, -23.2, -24.7,
           -23.0, -18.6, -12.4, -7.0]
```

For more detailed usage checkout
the [Demo notebook](https://github.com/spaulaus/dsp_toolkit/blob/master/docs/demo.ipynb).

## Module Descriptions

### filtering

Implements a simple trapezoidal filter without any bells and whistles. We also include a simple RC
low-pass filter used for conditioning signals.

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

Takes a user provided energy distribution (either binned or raw) and calculates signal pileups based
on trapezoidal filter parameters and count rates. We've also provided some macros that can be used
with the CERN ROOT program. Those scripts served as the basis for the python functions.

### timing

Provides both fitting and constant fraction discrimination (CFD) functions. We implement both a
traditional CFD, and a CFD described in XIA's Pixie-16 Manual. We implement a couple of different
fitting functions. The `vandle` function is the most tested and used function.


