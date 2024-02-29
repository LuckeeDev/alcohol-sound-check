import numpy as np
import string


def get_distance(spectrum_1, spectrum_2):
    return np.max(np.abs(spectrum_1 - spectrum_2))


# This is not needed
def get_normalisation_distance(references):
    normalisation_distances = []

    for index in range(len(references)):
        ref = references[index]
        other_references = references[:index] + references[index + 1 :]

        distances_norminf = np.array(
            [get_distance(ref[1], other_ref[1]) for other_ref in other_references]
        )
        mean_distance = np.mean(distances_norminf)
        normalisation_distances.append(mean_distance)

    return np.mean(normalisation_distances)


def exponential(x, a, b, c):
    return a * np.exp(b * x) + c


def format_plot_title(label: str):
    words = label.split("_")
    title = " ".join(words)
    return string.capwords(title)
