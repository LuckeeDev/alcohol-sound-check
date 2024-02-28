import matplotlib.pyplot as plt
import audio
import os
import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize
import librosa

AUDIO_FOLDER = input("Enter the path of the audio folder: ")


def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c


for dir_name in os.listdir(AUDIO_FOLDER):
    references = []
    points_norm1 = []
    points_norminf = []

    dir_path = os.path.join(AUDIO_FOLDER, dir_name)
    reference_folder = os.path.join(dir_path, "reference")

    for file_name in os.listdir(reference_folder):
        file_path = os.path.join(reference_folder, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)
        references.append((frequencies, spectrum))

    effect_folder = os.path.join(dir_path, "effect")

    for file_name in os.listdir(effect_folder):
        file_path = os.path.join(effect_folder, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)

        distances_norm1 = np.array(
            [
                integrate.simpson(
                    np.abs(spectrum[1:] - ref[1][1:]), x=np.log10(frequencies[1:])
                )
                for ref in references
            ]
        )
        distance_norm1 = np.mean(distances_norm1)
        points_norm1.append(distance_norm1)

        distances_norminf = np.array(
            [np.max(np.abs(spectrum - ref[1])) for ref in references]
        )
        distance_norminf = np.mean(distances_norminf)
        points_norminf.append(distance_norminf)

    x_values = np.linspace(0, len(points_norm1) - 1, len(points_norm1))

    popt = optimize.curve_fit(exponential, x_values, points_norminf, p0=[15, 1, 30])

    plt.figure(figsize=(12, 10))
    plt.scatter(x_values, points_norm1, label="Norm 1")
    plt.scatter(x_values, points_norminf, label="Norm inf")
    plt.plot(x_values, exponential(x_values, *popt[0]), "r", label="Fit")
    plt.xlabel("Index")
    plt.ylabel("Distances")
    plt.title("Distances Plot")
    plt.legend()

    fig_path = os.path.join(dir_path, f"{dir_name}.pdf")
    plt.savefig(fig_path)
