import matplotlib.pyplot as plt
import audio
import os
import numpy as np
import scipy.integrate as integrate
import librosa

REFERENCE_FOLDER = input("Input reference folder: ")
EFFECT_FOLDER = input("Input effect folder: ")

references = []
points_norm1 = []
points_norminf = []

for file_name in os.listdir(REFERENCE_FOLDER):
    file_path = os.path.join(REFERENCE_FOLDER, file_name)
    y, sr = librosa.load(file_path)

    frequencies, spectrum = audio.get_spectrum(y, sr)
    references.append((frequencies, spectrum))

for file_name in os.listdir(EFFECT_FOLDER):
    file_path = os.path.join(EFFECT_FOLDER, file_name)
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
plt.scatter(x_values, points_norm1, label="Norm 1")
plt.scatter(x_values, points_norminf, label="Norm inf")
plt.xlabel("Index")
plt.ylabel("Distances")
plt.title("Distances Plot")
plt.legend()
plt.show()
