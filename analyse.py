import numpy as np


def get_distance(spectrum_1, spectrum_2):
    return np.max(np.abs(spectrum_1 - spectrum_2))


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
