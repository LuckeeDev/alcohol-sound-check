import numpy as np
import string


def get_distance(norm, spectrum, references, frequencies=None):
    distances = np.array([])

    if frequencies is None:
        distances = np.array([norm(spectrum, ref[1]) for ref in references])
    else:
        distances = np.array(
            [norm(spectrum, ref[1], frequencies) for ref in references]
        )

    return np.mean(distances), np.std(distances)


def exponential(x, a, b, c):
    return a * np.exp(b * x) + c


def final_fit(x, a):
    return [a * eta * h / (rho) for (eta, rho, h) in x]


def format_plot_title(label: str):
    words = label.split("_")
    title = " ".join(words)
    return string.capwords(title)


def get_error(x, a, b, delta_a, delta_b, delta_c):
    a_err = np.exp(b * x) * delta_a
    b_err = a * x * np.exp(b * x) * delta_b
    c_err = delta_c

    return a_err + b_err + c_err
