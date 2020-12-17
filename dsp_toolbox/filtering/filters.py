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
