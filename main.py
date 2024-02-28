import matplotlib.pyplot as plt
import audio
import os
import numpy as np
import scipy.integrate as integrate

REFERENCE_FOLDER = input("Input reference folder: ")
EFFECT_FOLDER = input("Input effect folder: ")

references = []
points = []

for file_name in os.listdir(REFERENCE_FOLDER):
    file_path = os.path.join(REFERENCE_FOLDER, file_name)
    frequencies, spectrum = audio.get_spectrum(file_path)
    references.append((frequencies, spectrum))

for file_name in os.listdir(EFFECT_FOLDER):
    file_path = os.path.join(EFFECT_FOLDER, file_name)
    frequencies, spectrum = audio.get_spectrum(file_path)
    distances = np.array(
        [
            integrate.simpson(
                np.abs(spectrum[1:] - ref[1][1:]), x=np.log10(frequencies[1:])
            )
            for ref in references
        ]
    )
    distance = np.mean(distances)
    points.append(distance)

x_values = np.linspace(0, len(points) - 1, len(points))
plt.plot(x_values, points)
plt.xlabel("Index")
plt.ylabel("Distances")
plt.title("Distances Plot")
plt.show()
