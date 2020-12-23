"""
file: fitters.py
brief:
author: S. V. Paulauskas
date: December 23, 2020
"""
import numpy as np
from scipy.optimize import curve_fit


def crystal_ball(data, mu, amplitude, alpha, n, sigma):
    """
    The Crystal Ball function is defined here: https://en.wikipedia.org/wiki/Crystal_Ball_function
    It's really a probability density function.

    double t = (x[0] - mu) / sigma;

    if (alpha < 0)
        t = -t;

    double absAlpha = fabs(alpha);

    if (t >= -absAlpha) {
        return amplitude * exp(-0.5 * t * t) + baseline_;
    } else {
        double a = pow(n / absAlpha, n) * exp(-0.5 * absAlpha * absAlpha);
        double b = n / absAlpha - absAlpha;
        return amplitude * a / pow(b - t, n) + baseline_;
    }

    :param data:
    :param mu:
    :param amplitude:
    :param alpha:
    :param n:
    :param sigma:
    :return:
    """
    pass


def csi(data, phase, amplitude, n, tau):
    """
    This function is primarily used for fitting CsI(Na) detector signals.

    double xprime0 = (x[0] - phase) / tau0;
    double val;
    if (x[0] < phase)
        val = baseline_;
    else
        val = amp * pow(xprime0 / tau0, n) * exp(-xprime0) + baseline_;
    return (val);

    :param data:
    :param phase:
    :param amplitude:
    :param n:
    :param tau:
    :return:
    """
    pass


def emcal(data, phase, amplitude, n, tau):
    """
    Found this somewhere being used to fit signals from an EM Calorimeter. Can't find the origianl
    reference anymore.

    double xprime = (x[0] - phase) / tau;
    double val;
    if (x[0] < phase)
        val = baseline_;
    else
        val = amp * pow(xprime, n) * exp(-xprime) + baseline_;
    return (val);

    :param data:
    :param phase:
    :param amplitude:
    :param n:
    :param tau:
    :return:
    """
    pass


def sipmt_fast(data, phase, amplitude, sigma):
    """
    Used to fit the fast output signals from the SiPMT arrays at UTK.

    double diff = x[0] - phase;
    double val =
            (amp / (sigma * sqrt(2 * M_PI))) *
            exp(-diff * diff / (2 * sigma * sigma)) + baseline_;
    return (val);

    :param data:
    :param phase:
    :param amplitude:
    :param sigma:
    :return:
    """
    pass


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
