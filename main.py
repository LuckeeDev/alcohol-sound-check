import matplotlib.pyplot as plt
import audio
import analyse
import os
import numpy as np
import scipy.optimize as optimize
import librosa
from label_timer import LabelTimer

AUDIO_FOLDER = input("Enter the path of the audio folder: ")
LABELS_FILE_NAME = "labels.txt"


for dir_name in os.listdir(AUDIO_FOLDER):
    dir_path = os.path.join(AUDIO_FOLDER, dir_name)

    labels_file_path = os.path.join(dir_path, LABELS_FILE_NAME)
    timer = LabelTimer(labels_file_path)

    references = []
    reference_folder_path = os.path.join(dir_path, "reference")

    for file_name in os.listdir(reference_folder_path):
        file_path = os.path.join(reference_folder_path, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)
        references.append((frequencies, spectrum))

    t_values = []
    data_points = []
    effect_folder = os.path.join(dir_path, "effect")

    for file_name in os.listdir(effect_folder):
        t_values.append(timer(file_name))

        file_path = os.path.join(effect_folder, file_name)
        y, sr = librosa.load(file_path)

        frequencies, spectrum = audio.get_spectrum(y, sr)

        distances = np.array(
            [
                analyse.get_distance(spectrum[1:], ref[1][1:], frequencies[1:])
                for ref in references
            ]
        )
        mean_distance = np.mean(distances)
        data_points.append(mean_distance)

    popt, _ = optimize.curve_fit(
        analyse.exponential, t_values, data_points, p0=[10, -1 / 10, 5]
    )
    height = popt[2]

    plt.figure(figsize=(12, 10))
    plt.scatter(t_values, data_points - height, label="Norm: 1 with log scale")

    t_values = np.sort(t_values)
    plt.plot(
        t_values,
        [analyse.exponential(t, *popt) - height for t in t_values],
        "r",
        label="Fit",
    )
    plt.legend()

    plt.xlabel("Time (s)")
    plt.ylabel("Distance")
    plot_title = analyse.format_plot_title(dir_name)
    plt.title(plot_title)

    plt.grid(True)
    plt.margins(x=0)
    plt.xlim(left=0)

    fig_path = os.path.join(dir_path, f"{dir_name}.pdf")
    plt.savefig(fig_path)
    print(f"Done {plot_title}")
