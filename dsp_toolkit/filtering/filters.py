"""
file: filters.py
brief:
author: S. V. Paulauskas
date: December 17, 2020
"""


def calculate_trapezoidal_filter(data, length, gap):
    if len(data) < 2 * length + gap + 1:
        return ValueError(f"Filter length ({2 * length + gap}) exceeds data length ({len(data)})")

    trap_filter = [0] * len(data)
    for i in range(2 * length + gap, len(data)):
        trap_filter[i] = ((sum(data[i - length + 1:i]) - sum(
            data[i - 2 * length - gap + 1: i - length - gap])) / length)

    return trap_filter


def calculate_rc_lowpass_filter(data, time_constant, time_interval):
    """
    This code can be found at https://en.wikipedia.org/wiki/Low-pass_filter
    :param data: 
    :param time_constant: 
    :param time_interval: 
    :return: 
    """
    result = [0] * len(data)
    alpha = time_interval / (time_constant + time_interval)
    result[0] = alpha * data[0]

    for i in range(1, len(data)):
        result[i] = result[i - 1] + alpha * (data[i] - result[i - 1])

    return result
