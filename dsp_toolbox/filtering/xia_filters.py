"""
file: xia_filters.py
brief:
author: S. V. Paulauskas
date: December 14, 2020
"""
from math import exp
from statistics import mean

from dsp_toolbox.filtering.filters import calculate_trapezoidal_filter


# TODO: Add the esums to the output!

def calculate_baseline(data, trigger, length):
    offset = trigger - length - 5
    if offset < 0:
        raise ValueError("First trigger happened too early to calculate the baseline!")
    return mean(data[:offset])


def calculate_energy_filter_coefficients(length, decay_constant):
    if decay_constant == 0:
        raise ValueError("Decay constant must be non-zero!")

    beta = exp(-1.0 / decay_constant)

    if beta == TypeError:
        raise beta

    cg = 1 - beta
    ctmp = 1 - pow(beta, length)

    return {'beta': beta, "rise": -(cg / ctmp) * pow(beta, length), "gap": cg, "fall": cg / ctmp}


def calculate_energy_filter_limits(trigger_position, length, gap, data_length):
    min_limit = trigger_position - length - 10
    if min_limit < 0:
        raise ValueError("Trigger happened too early in the trace to calculate the energy!")
    if trigger_position + length + gap > data_length:
        raise ValueError("Trigger happened too late in the trace to calculate the energy!")

    return {"rise": (min_limit, min_limit + length - 1),
            "gap": (min_limit + length, min_limit + length + gap - 1),
            "fall": (min_limit + length + gap, min_limit + 2 * length + gap - 1)}


def calculate_energy(data, baseline, coefficients, limits):
    data_without_baseline = [x - baseline for x in data]
    sum_rise = sum(data_without_baseline[limits['rise'][0]: limits['rise'][1]])
    sum_gap = sum(data_without_baseline[limits['gap'][0]: limits['gap'][1]])
    sum_fall = sum(data_without_baseline[limits['fall'][0]: limits['fall'][1]])

    return coefficients['rise'] * sum_rise + coefficients['gap'] * sum_gap + coefficients[
        'fall'] * sum_fall, {'rising_sum': sum_rise, 'gap_sum': sum_gap, 'falling_sum': sum_fall}


def calculate_energy_filter(data, length, gap, baseline, coefficients):
    if not data:
        raise ValueError("Data length cannot be less than 0")

    offset = 2 * length + gap - 1

    if len(data) < offset:
        raise ValueError(f"The data length({len(data)}) is too small for the requested filter "
                         f"size ({offset})!")

    data_no_baseline = [x - baseline for x in data]
    response = [0] * len(data)
    for x in range(offset, len(data_no_baseline)):
        esumL = sum(data_no_baseline[x - offset:x - offset + length])
        esumG = sum(data_no_baseline[x - offset + length: x - offset + length + gap])
        esumF = sum(data_no_baseline[x - offset + length + gap: x - offset + 2 * length + gap])
        response[x] = coefficients['rise'] * esumL + coefficients['gap'] * esumG + coefficients[
            'fall'] * esumF

    for x in range(0, offset):
        response[x] = response[offset]

    return response


def calculate_trigger_filter(data, length, gap, threshold):
    if not data:
        raise ValueError("Cannot calculate a filter without some data!")

    has_recrossed = False
    triggers = list()
    trigger_filter = calculate_trapezoidal_filter(data, length, gap)

    for val in trigger_filter:
        if val >= threshold:
            if not triggers:
                triggers.append(trigger_filter.index(val))
            if has_recrossed:
                triggers.append(trigger_filter.index(val))
                has_recrossed = False
        else:
            if triggers:
                has_recrossed = True

    if not triggers:
        raise ValueError("No triggers found in the provided data!")

    return triggers, trigger_filter


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from dsp_toolbox.sample_data import sample_traces as st

    signal = st.plastic_scintillator

    trig_params = {"l": 15, "g": 5, "t": 10}
    triggers, trigger_filter = calculate_trigger_filter(signal, trig_params['l'],
                                                        trig_params['g'], trig_params['t'])
    baseline = calculate_baseline(signal, triggers[0], trig_params['l'])

    energy_params = {"l": 10, "g": 5, "t": 2.5}
    energy_filter_coefficients = calculate_energy_filter_coefficients(energy_params['l'],
                                                                      energy_params['t'])
    energy, energy_sums = calculate_energy(signal, baseline, energy_filter_coefficients,
                                           calculate_energy_filter_limits(triggers[0],
                                                                          energy_params['l'],
                                                                          energy_params['g'],
                                                                          len(signal)))
    energy_filter = calculate_energy_filter(signal, energy_params['l'],
                                            energy_params['g'], baseline,
                                            energy_filter_coefficients)

    plt.plot(signal, label="Data")
    plt.plot(trigger_filter, label="Trigger Filter")
    plt.plot(energy_filter, label="Energy Filter")
    for trigger in triggers:
        plt.axvline(x=trigger, color='purple', label="Trigger")
    plt.hlines(y=baseline, xmin=triggers[0] - 10, xmax=len(signal), colors='red',
               label="Baseline")
    plt.legend()
    plt.xlabel("Bin")
    plt.ylabel('Adc Units / Bin')
    plt.title(f"Calculated energy: {round(energy, 2)}")
    plt.xlim([round(0.75 * triggers[0]), len(signal)])
    plt.show()
