import numpy as np
from constants import *


THRESHOLD = 0.001


def get_amp(x):
    return abs(x)


# TODO: correction
def get_phase(x):
    return - np.arctan2(np.imag(x), np.real(x))


def fft(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if N == 1:
        return x
    elif N % 2 > 0:
        raise ValueError("Size of x must be a power of 2")
    else:
        X_even = fft(x[::2])
        X_odd = fft(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        result = np.concatenate([X_even + factor[:N // 2] * X_odd,
                                 X_even + factor[N // 2:] * X_odd])
        return result


def get_spectrum_from_fft(fft_result, harmonic_amount):
    amplitudes = [get_amp(fft_result[i + 1]) * 2 / N for i in range(harmonic_amount)]
    phases = [get_phase(fft_result[i + 1]) if amplitudes[i] > THRESHOLD else 0 for i in range(harmonic_amount)]
    return list(zip(amplitudes, phases))


def get_fft_spectrum(signal, harmonic_amount):
    fft_result = fft(signal)
    return get_spectrum_from_fft(fft_result, harmonic_amount)
