"""
file: constant_fraction_discriminators.py
brief:
author: S. V. Paulauskas
date: December 16, 2020
"""
from statistics import mean


def calculate_traditional_cfd(data, delay, fraction):
    if len(data) < delay or len(data) < 10:
        raise ValueError(f"Not enough data points ({len(data)}) for the delay ({delay})!!")
    if not 0 < fraction < 1:
        raise ValueError(f"Fraction must a value between 0 and 1!")
    if not -10 < mean(data[0:10]) < 10:
        raise ValueError("You need to provide us with a baseline subtracted trace so we can find "
                         "the zero crossing point!")
    cfd_response = [x - fraction * data[i + delay] for i, x in enumerate(data[0:len(data) - delay])]

    x2 = cfd_response.index(next(filter(lambda x: x > 0, cfd_response[cfd_response.index(
        min(cfd_response)): cfd_response.index(max(cfd_response))])))
    y2 = cfd_response[x2]
    x1 = x2 - 1
    y1 = cfd_response[x1]

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    return -intercept / slope, cfd_response


def calculate_xia_cfd(trigger_response, delay, scaling_factor):
    """
    This function is paraphrased from XIA's Pixie16 User's Manual v 3.0 page 45.
    :param trigger_response:
    :param delay:
    :param scaling_factor:
    :return:
    """
    if len(trigger_response) < delay:
        raise ValueError(f"Not enough data points ({len(trigger_response)}) for "
                         f"the delay ({delay})!!")
    if not 1 < scaling_factor < 7 or not isinstance(scaling_factor, int):
        raise ValueError(f"Scaling factor must be an integer between 1 and 7!")

    cfd_response = [trigger_response[i + delay] * (1. - scaling_factor / 8.) - x for i, x in
                    enumerate(trigger_response[0:len(trigger_response) - delay])]

    min_pos = cfd_response.index(min(cfd_response))
    max_pos = cfd_response.index(max(cfd_response[0:min_pos]))

    x2 = cfd_response.index(next(filter(lambda x: x < 0, cfd_response[max_pos:min_pos])))
    y2 = cfd_response[x2]
    x1 = x2 - 1
    y1 = cfd_response[x1]

    return x1 + (y1 / (y1 - y2)), cfd_response


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from dsp_toolbox.sample_data import sample_traces as st
    from dsp_toolbox.filtering.xia_filters import (calculate_baseline,
                                                   calculate_trigger_filter)

    signal = st.csi
    filter_triggers, trig_filter = calculate_trigger_filter(signal, 40, 10, 10)
    baseline = calculate_baseline(signal, filter_triggers[0], 40)

    trad_trigger, trad_response = calculate_traditional_cfd([x - baseline for x in signal], 30,
                                                            0.50)
    xia_trigger, xia_response = calculate_xia_cfd(trig_filter, 10, 4)

    plt.plot([x - baseline for x in signal], label='Data')
    plt.plot(trad_response, label="Trad. CFD")
    plt.axvline(x=trad_trigger, color='purple', label="Trad. CFD - Trigger")
    plt.plot(xia_response, label="XIA CFD")
    plt.axvline(x=xia_trigger, color='yellow', label="XIA CFD - Trigger")
    plt.hlines(y=0, xmin=0, xmax=len(signal), colors='red', label="Zero")
    plt.legend()
    plt.xlim([round(0.75 * trad_trigger), round(1.25 * trad_trigger)])
    plt.show()
