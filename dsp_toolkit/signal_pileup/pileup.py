"""
file: pileup.py
brief:
author: S. V. Paulauskas
date: December 18, 2020
"""
from math import exp, log
from random import uniform

from numpy import arange, unique, random


def calculate_pileup_probability(rate, length, gap):
    """
    Equation taken from the following paper.
    https://dx.doi.org/10.1016/j.nima.2007.05.323

    In the case of XIA's Pixie-16 modules, we don't have pre-pileup. The first signal would
    presumably be our trigger in this situation. That means we only have post-pileup.

    :param rate: The detector rate in seconds
    :param length: The filter length in seconds
    :param gap: The filter gap in seconds.
    :return: The expected probability of a pileup
    """
    x = rate * (2 * length + gap)
    return (1 + x) * (1 - exp(-2 * x))


def signal_function(t, rise_time, decay_time):
    """
    :param t: The signal time in seconds
    :param rise_time: The signal rise time in seconds.
    :param decay_time: The signal decay time in seconds.
    :return: The signal at time t
    """
    if t < 0:
        return 0
    if 0 <= t < rise_time:
        return t / rise_time
    return exp(-(t - rise_time) / decay_time)


def model_rectangular_pulses(pileup_time, energy1, energy2, cfg):
    """
    Models the pileup energy using a rectangular pulse. Depends on the following parameters:
        * Filter gap or flat top in seconds
        * Filter length or rise time in seconds

    :param pileup_time: The time that the pile-up occurred in seconds
    :param energy1: The energy of the first signal we had.
    :param energy2: The energy of the piled-up signal
    :param cfg: The configuration containing all necessary parameters.
    :return: The piled up energy
    """
    if pileup_time <= cfg['filter']['gap']:
        return energy1 + energy2
    if cfg['filter']['gap'] < pileup_time <= cfg['filter']['length'] + cfg['filter']['gap']:
        return energy1 + energy2 * (
                1. - (pileup_time - cfg['filter']['gap']) / cfg['filter']['length'])
    return 0.0


def model_trapezoidal_pulses(pileup_time, energy1, energy2, cfg):
    """
    Models the pileup energy based on a trapezoidal filter. We have 4 scenarios for the pileup.
    The final energy depends on when the pileup signal peaks:
        1. fully inside the gap of the first signal,
        2. between the gap and the rise time of the first signal,
        3. fully inside the first signal's peak,
        4. or at the end of the first signal's peak.

    Depends on the following parameters:
        * Filter gap or flat top in seconds
        * Filter length or rise time in seconds
        * Signal rise time in seconds

    :param pileup_time: The time that the pile-up occurred in seconds
    :param energy1: The energy of the first signal we had.
    :param energy2: The energy of the piled-up signal
    :param cfg: The configuration containing all necessary parameters.
    :return: The piled up energy
    """
    if pileup_time <= cfg['filter']['gap'] - cfg['signal']['rise_time']:
        # Second pulse rises fully inside gap
        return energy1 + energy2
    if cfg['filter']['gap'] - cfg['signal']['rise_time'] < pileup_time <= cfg['filter']['gap']:
        # Second pulse rises between gap and filter risetime
        x = pileup_time + cfg['signal']['rise_time'] - cfg['filter']['gap']
        y = x * energy2 / cfg['signal']['rise_time']
        a = x * y / 2
        return energy1 + (energy2 * cfg['filter']['length'] - a) / cfg['filter']['length']
    if cfg['filter']['gap'] < pileup_time <= cfg['filter']['gap'] + cfg['filter'][
        'length'] - cfg['signal']['rise_time']:
        # Second pulse rises fully inside the peak
        return energy1 + (
                cfg['filter']['length'] + cfg['filter']['gap'] - pileup_time - 0.5
                * cfg['signal']['rise_time']) * energy2 / cfg['filter']['length']
    if cfg['filter']['gap'] + cfg['filter']['length'] - cfg['signal']['rise_time'] < pileup_time <= \
            cfg['filter']['gap'] + cfg['filter']['length']:
        # Second pulse rises at the end of the peak
        x = cfg['filter']['length'] + cfg['filter']['gap'] - pileup_time
        y = x * energy2 / cfg['signal']['rise_time']
        return energy1 + x * y * 0.5 / cfg['filter']['length']


def model_arbitrary_pulse_shape(pileup_time, energy1, energy2, cfg):
    """
    This signal is arbitrary in the sense that it has a rise time and a single exponential decay.
    It does not mean any arbitrary shape. We use a basic summing integration to figure out
    the pile-up energy.

    Depends on the following parameters:
        * Filter gap or flat top in seconds
        * Filter length or rise time in seconds
        * Signal rise time in seconds
        * Digitizer sampling interval in seconds. Ex. 100 MHz -> 10e-9 s

    :param pileup_time: The time that the pile-up occurred in seconds
    :param energy1: The energy of the first signal we had.
    :param energy2: The energy of the piled-up signal
    :param cfg: The configuration containing all necessary parameters.
    :return: The piled up energy
    """
    integral = 0
    normalization = 0
    for t in arange(cfg['filter']['gap'], cfg['filter']['length'] + cfg['filter']['gap'],
                    cfg['sampling_interval']):
        integral = integral + energy1 * signal_function(t, cfg['signal']['rise_time'],
                                                        cfg['signal'][
                                                            'decay_time']) + energy2 * signal_function(
            t - pileup_time, cfg['signal']['rise_time'], cfg['signal']['decay_time'])
        normalization = normalization + 1
    return integral / normalization


def model_xia_pixie16_filter(pileup_time, energy1, energy2, cfg):
    """
    Simulates piled up events based on XIA's Pixie-16 Energy filter sums. These sums are basically
    a trapezoidal filter. The filter sums are multiplied by coefficients to take into account
    signals sitting on the tail of the previous pulse. See
    https://doi.org/10.1109/NSSMIC.2008.4774600 for more information.

    Depends on the following parameters:
        * Filter gap or flat top in seconds
        * Filter length or rise time in seconds
        * Filter tau in seconds
        * Signal rise time in seconds
        * Signal decay time in seconds
        * Digitizer sampling interval in seconds. Ex. 100 MHz -> 10e-9 s

    :param pileup_time: The time that the pile-up occurred in seconds
    :param energy1: The energy of the first signal we had.
    :param energy2: The energy of the piled-up signal
    :param cfg: The configuration containing all necessary parameters.
    :return: The piled up energy
    """
    gap_sum = sum([energy1 * signal_function(t, cfg['signal']['rise_time'], cfg['signal'][
        'decay_time']) + energy2 * signal_function(t - pileup_time,
                                                   cfg['signal']['rise_time'],
                                                   cfg['signal']['decay_time']) for t in
                   arange(0, cfg['filter']['gap'], cfg['sampling_interval'])])
    fall_sum = sum([energy1 * signal_function(t, cfg['signal']['rise_time'], cfg['signal'][
        'decay_time']) + energy2 * signal_function(t - pileup_time,
                                                   cfg['signal']['rise_time'],
                                                   cfg['signal']['decay_time']) for t in
                    arange(cfg['filter']['gap'], cfg['filter']['length'] + cfg['filter']['gap'],
                           cfg['sampling_interval'])])

    b = exp(-cfg['sampling_interval'] / cfg['filter']['tau'])
    Cg = 1. - b
    C1 = (1. - b) / (1. - b ** (cfg['filter']['length'] / cfg['sampling_interval']))
    return Cg * gap_sum + C1 * fall_sum


def generate_pileups(cfg, model, distribution, weights=None):
    """
    Main driver to generate pile-up events. We take the information from the config file for use
    with calculating our pileup times and energies. We take in a distribution, which we sample in
    order to generate the energies in our spectrum. If we are given weights we'll use those weights
    to weigh the energy distribution, if we don't have weights, we'll calculate them. The length of
    the distribution and weight lists must be the same.

    All times in the configuration file are expected to be in seconds!

    :param cfg: The configuration file containing
    :param model:
    :param distribution:
    :param weights:
    :return: The simulated energy and pileup distributions
    """
    if weights and len(distribution) != len(weights):
        raise ValueError("The energy distribution and its weights must be the same length!")

    if not weights:
        choices, counts = unique([round(x) for x in distribution], return_counts=True)
        weights = [x / sum(counts) for x in counts]
    else:
        choices = distribution

    signal = list()
    pileup = list()
    while len(signal) + len(pileup) < cfg['number_of_events']:
        signal.append(random.choice(choices, 1, p=weights)[0] + uniform(0, 1))
        energy2 = random.choice(choices, 1, p=weights)[0] + uniform(0, 1)

        time = -log(1. - uniform(0, 1)) / cfg['event_rate']
        if time <= cfg['filter']['length'] + cfg['filter']['gap']:
            pileup.append(model(time, signal[-1], energy2, cfg))
        else:
            signal.append(energy2)
    return signal, pileup


if __name__ == '__main__':
    from random import gauss
    import matplotlib.pyplot as plt

    # All times are expected to be in seconds.
    configuration = {
        "event_rate": 41600,
        "number_of_events": 1000000,
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

    distribution = [gauss(100, 1) for x in range(0, configuration['event_rate'])]
    signal, pileup = generate_pileups(configuration, model_xia_pixie16_filter, distribution)

    bins = 300
    plt.hist(signal, label='signal', bins=bins, range=[0, bins])
    plt.hist(pileup, label='pileup', bins=bins, range=[0, bins], alpha=0.5)
    plt.gca().set(xlabel="Energy (arb)", ylabel='Energy (arb) / bin', title=f"Pileup simulation", yscale='log')
    plt.show()
