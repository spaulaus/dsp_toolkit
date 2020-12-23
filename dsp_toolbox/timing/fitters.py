"""
file: fitters.py
brief:
author: S. V. Paulauskas
date: December 23, 2020
"""
import numpy as np
from scipy.optimize import curve_fit


def vandle(data, phase, amplitude, beta, gamma):
    """
    The standard VANDLE timing function used to fit plastic scintillator signals for high resolution
    timing applications. See https://doi.org/10.1016/j.nima.2013.11.028 for more details about
    the performance of this function.
    :param data: The data array
    :param phase: The trigger time of the signal
    :param amplitude: The height of the signal
    :param beta: Decay constant of the exponential tail
    :param gamma: Width of the inverted Gaussian on the signal's leading edge.
    :return:
    """
    return np.piecewise(data, [data < phase, data >= phase],
                        [lambda t: 0.0, lambda t: amplitude * np.exp(-beta * (t - phase)) * (
                                    1 - np.exp(-pow(gamma * (t - phase), 4.)))])


if __name__ == '__main__':
    from statistics import mean
    import matplotlib.pyplot as plt
    from dsp_toolbox.sample_data.sample_traces import plastic_scintillator as ps

    baseline = mean(ps[0:60])
    ydata = np.array([x - baseline for x in ps])
    xdata = np.array(range(0, len(ps)))

    results, pcov = curve_fit(vandle, xdata, ydata, p0=[ps.index(max(ps)), max(ps), 0.3, 0.3])

    plt.plot(ydata, label='Signal', color='blue')
    plt.plot(xdata, vandle(xdata, *results), label='Fit', color='red')
    plt.axvline(x=results[0], color='purple', label="Trigger")
    plt.legend()
    plt.show()
