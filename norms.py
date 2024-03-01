import scipy.integrate as integrate
import numpy as np


def l1_log(spectrum_1, spectrum_2, frequencies):
    mask = [20 <= f <= 18000 for f in frequencies]

    return integrate.simpson(
        np.abs(spectrum_1[mask] - spectrum_2[mask]),
        x=np.log(frequencies[mask]),
    )


def chebyshev(spectrum_1, spectrum_2):
    return np.max(np.abs(spectrum_1 - spectrum_2))


def l1(spectrum_1, spectrum_2, frequencies):
    return integrate.simpson(np.abs(spectrum_1 - spectrum_2), x=frequencies)


def mean(spectrum_1, spectrum_2):
    return np.mean(np.abs(spectrum_1 - spectrum_2))
