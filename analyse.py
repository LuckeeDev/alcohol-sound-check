import numpy as np
import string
import scipy.integrate as integrate


def get_distance(spectrum_1, spectrum_2, frequencies):
    return integrate.simpson(np.abs(spectrum_1 - spectrum_2), x=np.log(frequencies))


def exponential(x, a, b, c):
    return a * np.exp(b * x) + c


def format_plot_title(label: str):
    words = label.split("_")
    title = " ".join(words)
    return string.capwords(title)
