"""
file: pileup.py
brief:
author: S. V. Paulauskas
date: December 18, 2020
"""
from math import exp, log
from random import uniform, gauss

from numpy import arange


def signal_function(t, rise_time, decay_time):
    """
    :param t:
    :param rise_time:
    :param decay_time:
    :return:
    """
    if t < 0:
        return 0
    if 0 <= t < rise_time:
        return t / rise_time
    return exp(-(t - rise_time) / decay_time)


def model_rectangular_pulses(energy1, energy2, cfg):
    """
    :param cfg:
    :param energy1:
    :param energy2:
    :return:
    """
    if cfg['sampling_interval'] <= cfg['filter']['gap']:
        return energy1 + energy2
    if cfg['filter']['gap'] < cfg['sampling_interval'] <= cfg['filter']['length'] + cfg['filter']['gap']:
        return energy1 + energy2 * (1. - (cfg['sampling_interval'] - cfg['filter']['gap']) / cfg['filter']['length'])
    return 0.0


def model_trapezoidal_pulses(energy1, energy2, cfg):
    """
    :param cfg:
    :param energy1:
    :param energy2:
    :return:
    """
    if cfg['sampling_interval'] <= cfg['filter']['gap'] - cfg['signal']['rise_time']:
        # Second pulse rises fully inside gap
        return energy1 + energy2
    if cfg['filter']['gap'] - cfg['signal']['rise_time'] < cfg['sampling_interval'] <= cfg['filter']['gap']:
        # Second pulse rises between gap and filter risetime
        x = cfg['sampling_interval'] + cfg['signal']['rise_time'] - cfg['filter']['gap']
        y = x * energy2 / cfg['signal']['rise_time']
        a = x * y / 2
        return energy1 + (energy2 * cfg['filter']['length'] - a) / cfg['filter']['length']
    if cfg['filter']['gap'] < cfg['sampling_interval'] <= cfg['filter']['gap'] + cfg['filter']['length'] - cfg['signal']['rise_time']:
        # Second pulse rises fully inside the peak
        return energy1 + (cfg['filter']['length'] + cfg['filter']['gap'] - cfg['sampling_interval'] - 0.5
                          * cfg['signal']['rise_time']) * energy2 / cfg['filter']['length']
    if cfg['filter']['gap'] + cfg['filter']['length'] - cfg['signal']['rise_time'] < cfg['sampling_interval'] <= cfg['filter']['gap'] + cfg['filter']['length']:
        # Second pulse rises at the end of the peak
        x = cfg['filter']['length'] + cfg['filter']['gap'] - cfg['sampling_interval']
        y = x * energy2 / cfg['signal']['rise_time']
        return energy1 + x * y * 0.5 / cfg['filter']['length']


def model_arbitrary_pulse_shape(energy1, energy2, cfg):
    """
    :param cfg:
    :param energy1:
    :param energy2:
    :return:
    """
    integral = 0
    normalization = 0
    for t in arange(cfg['filter']['gap'], cfg['filter']['length'] + cfg['filter']['gap'], cfg['sampling_interval']):
        integral = integral + energy1 * signal_function(t, cfg['signal']['rise_time'], cfg['signal']['decay_time']) + energy2 * signal_function(t - cfg['sampling_interval'], cfg['signal']['rise_time'], cfg['signal']['decay_time'])
        normalization = normalization + 1
    return integral / normalization


def model_xia_pixie16_filter(energy1, energy2, cfg):
    """
    :param cfg:
    :param energy1:
    :param energy2:
    :return:
    """
    gap_sum = sum([energy1 * signal_function(t, cfg['signal']['rise_time'], cfg['signal'][
        'decay_time']) + energy2 * signal_function(t - cfg['sampling_interval'],
                                                   cfg['signal']['rise_time'],
                                                   cfg['signal']['decay_time']) for t in
                   arange(0, cfg['filter']['gap'], cfg['sampling_interval'])])
    fall_sum = sum([energy1 * signal_function(t, cfg['signal']['rise_time'], cfg['signal'][
        'decay_time']) + energy2 * signal_function(t - cfg['sampling_interval'],
                                                   cfg['signal']['rise_time'],
                                                   cfg['signal']['decay_time']) for t in
                    arange(cfg['filter']['gap'], cfg['filter']['length'] + cfg['filter']['gap'],
                           cfg['sampling_interval'])])

    b = exp(-cfg['sampling_interval'] / cfg['filter']['tau'])
    Cg = 1. - b
    C1 = (1. - b) / (1. - b ** (cfg['filter']['length'] / cfg['sampling_interval']))
    return Cg * gap_sum + C1 * fall_sum


def generate_pileups(model, cfg):
    signal = list()
    pileup = list()
    while cfg['number_of_events'] > 0:
        signal.append(gauss(10, 1.5))
        energy2 = signal[-1] + uniform(-1, 1)
        if -log(1. - uniform(0, 1)) / cfg['event_rate'] <= cfg['filter']['length'] + cfg['filter'][
            'gap']:
            pileup.append(model(signal[-1], energy2, cfg))
            cfg['number_of_events'] = cfg['number_of_events'] - 1
        else:
            signal.append(energy2)
            cfg['number_of_events'] = cfg['number_of_events'] - 2
    return signal, pileup


if __name__ == '__main__':
    from pandas import DataFrame
    import matplotlib.pyplot as plt

    # All times are expected to be in seconds.
    configuration = {
        "event_rate": 4.16e4,
        "number_of_events": 10000,
        "sampling_interval": 10.e-9,
        "signal": {
            # Parameters for CsI(Na)
            "rise_time": 0.10e-6,
            "decay_time": 0.76e-6
        },
        "filter": {
            "length": 0.20e-6,
            "gap": 0.64e-6,
            "tau": 0.86e-6
        }
    }

    signal, pileup = generate_pileups(model_xia_pixie16_filter, configuration)

    ax = plt.gca()
    ax.set(xlabel="Energy (arb)", ylabel='Energy (arb) / bin', title=f"Pileup simulation")
    ax.set_yscale('log')
    DataFrame(signal, columns=["signal"]).hist(bins=30, range=[0, 30], ax=ax, alpha=0.75).flatten()[
        0].get_figure().show()
    DataFrame(pileup, columns=["pileup"]).hist(bins=30, range=[0, 30], ax=ax, alpha=0.75).flatten()[
        0].get_figure().show()
