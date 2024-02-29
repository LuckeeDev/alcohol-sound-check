import scipy.integrate as integrate
import numpy as np


def l1_log(spectrum_1, spectrum_2, frequencies):
    return integrate.simpson(np.abs(spectrum_1 - spectrum_2), x=np.log(frequencies))


def chebyshev(spectrum_1, spectrum_2):
    return np.max(np.abs(spectrum_1 - spectrum_2))


def l1(spectrum_1, spectrum_2, frequencies):
    return integrate.simpson(np.abs(spectrum_1 - spectrum_2), x=frequencies)


def mean(spectrum_1, spectrum_2):
    return np.mean(np.abs(spectrum_1 - spectrum_2))
