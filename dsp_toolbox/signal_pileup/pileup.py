"""
file: pileup.py
brief:
author: S. V. Paulauskas
date: December 18, 2020
"""
from math import exp
from random import uniform, gauss

from numpy import arange, unique, random


def calculate_pileup_probability(rate, length, gap):
    """
    Equation taken from the following paper.
    https://dx.doi.org/10.1016/j.nima.2007.05.323

    :param rate: The detector rate in seconds
    :param length: The filter length in seconds
    :param gap: The filter gap in seconds.
    :return:
    """
    x = rate * (2 * length + gap)
    return (1 + x) * (1 - exp(-2 * x))


def signal_function(t, rise_time, decay_time):
    """
    :param t: The signal time in seconds
    :param rise_time: The signal rise time in seconds.
    :param decay_time: The signal decay time in seconds.
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
    if cfg['filter']['gap'] < cfg['sampling_interval'] <= cfg['filter']['length'] + cfg['filter'][
        'gap']:
        return energy1 + energy2 * (
                1. - (cfg['sampling_interval'] - cfg['filter']['gap']) / cfg['filter'][
            'length'])
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
    if cfg['filter']['gap'] - cfg['signal']['rise_time'] < cfg['sampling_interval'] <= \
            cfg['filter']['gap']:
        # Second pulse rises between gap and filter risetime
        x = cfg['sampling_interval'] + cfg['signal']['rise_time'] - cfg['filter']['gap']
        y = x * energy2 / cfg['signal']['rise_time']
        a = x * y / 2
        return energy1 + (energy2 * cfg['filter']['length'] - a) / cfg['filter']['length']
    if cfg['filter']['gap'] < cfg['sampling_interval'] <= cfg['filter']['gap'] + cfg['filter'][
        'length'] - cfg['signal']['rise_time']:
        # Second pulse rises fully inside the peak
        return energy1 + (
                cfg['filter']['length'] + cfg['filter']['gap'] - cfg['sampling_interval'] - 0.5
                * cfg['signal']['rise_time']) * energy2 / cfg['filter']['length']
    if cfg['filter']['gap'] + cfg['filter']['length'] - cfg['signal']['rise_time'] < cfg[
        'sampling_interval'] <= cfg['filter']['gap'] + cfg['filter']['length']:
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
    for t in arange(cfg['filter']['gap'], cfg['filter']['length'] + cfg['filter']['gap'],
                    cfg['sampling_interval']):
        integral = integral + energy1 * signal_function(t, cfg['signal']['rise_time'],
                                                        cfg['signal'][
                                                            'decay_time']) + energy2 * signal_function(
            t - cfg['sampling_interval'], cfg['signal']['rise_time'], cfg['signal']['decay_time'])
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


def generate_pileups(cfg, model, distribution, weights=None):
    signal = list()
    pileup = list()

    choices, counts = unique([round(x) for x in distribution], return_counts=True)
    if not weights:
        weights = [x / sum(counts) for x in counts]

    while cfg['number_of_events'] > 0:
        signal.append(random.choice(choices, 1, p=weights)[0] + uniform(0, 1))
        energy2 = round(signal[-1], 0) + uniform(0, 1)
        if uniform(0, 1) < configuration['pileup_probability']:
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
        "event_rate": 20000,
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

    configuration.setdefault('pileup_probability',
                             calculate_pileup_probability(configuration['event_rate'],
                                                          configuration['filter']['length'],
                                                          configuration['filter']['gap']))

    distribution = [gauss(15, 1.5) for x in range(0, configuration['event_rate'])]

    signal, pileup = generate_pileups(configuration, model_xia_pixie16_filter, distribution)

    ax = plt.gca()
    ax.set(xlabel="Energy (arb)", ylabel='Energy (arb) / bin', title=f"Pileup simulation")
    ax.set_yscale('log')
    DataFrame(signal, columns=["signal"]).hist(bins=30, range=[0, 30], ax=ax, alpha=0.75).flatten()[
        0].get_figure().show()
    DataFrame(pileup, columns=["pileup"]).hist(bins=30, range=[0, 30], ax=ax, alpha=0.75).flatten()[
        0].get_figure().show()
