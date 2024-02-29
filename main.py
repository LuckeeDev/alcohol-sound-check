import matplotlib.pyplot as plt
import audio
import analyse
import os
import numpy as np
import scipy.optimize as optimize
import librosa

AUDIO_FOLDER = input("Enter the path of the audio folder: ")


def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c


for dir_name in os.listdir(AUDIO_FOLDER):
    references = []
    points_norminf = []

    dir_path = os.path.join(AUDIO_FOLDER, dir_name)
    reference_folder = os.path.join(dir_path, "reference")

    for file_name in os.listdir(reference_folder):
        file_path = os.path.join(reference_folder, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)
        references.append((frequencies, spectrum))

    normalisation_distance = analyse.get_normalisation_distance(references)

    effect_folder = os.path.join(dir_path, "effect")

    for file_name in os.listdir(effect_folder):
        file_path = os.path.join(effect_folder, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)

        distances_norminf = np.array(
            [analyse.get_distance(spectrum, ref[1]) for ref in references]
        )
        mean_distance = np.mean(distances_norminf)
        points_norminf.append(mean_distance - normalisation_distance)

    x_values = np.linspace(0, len(points_norminf) - 1, len(points_norminf))

    popt = optimize.curve_fit(exponential, x_values, points_norminf, p0=[15, 1, 0])

    plt.figure(figsize=(12, 10))
    plt.scatter(x_values, points_norminf, label="Norm to infinity")
    plt.plot(x_values, exponential(x_values, *popt[0]), "r", label="Fit")
    plt.legend()

    plt.xlabel("Index")
    plt.ylabel("Distances")
    plt.title("Distances Plot")

    plt.ylim(bottom=0)
    plt.margins(x=0)

    fig_path = os.path.join(dir_path, f"{dir_name}.pdf")
    plt.savefig(fig_path)
