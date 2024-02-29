import matplotlib.pyplot as plt
import audio
import analyse
import norms
import os
import numpy as np
import scipy.optimize as optimize
import librosa
from label_timer import LabelTimer
from results_writer import ResultsWriter

AUDIO_FOLDER = input("Enter the path of the audio folder: ")
RESULTS_FILE = input("Enter the path of the results file: ")
LABELS_FILE_NAME = "labels.txt"

results = ResultsWriter(RESULTS_FILE)


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

        distance = analyse.get_distance(norms.l1_log, spectrum, references, frequencies)
        data_points.append(distance)

    popt, _ = optimize.curve_fit(
        analyse.exponential, t_values, data_points, p0=[10, -1 / 10, 5]
    )
    results.addline(
        {
            "id": dir_name,
            "norm_id": "l1_log",
            "exponent": popt[1],
            "intensity": analyse.exponential(0, *popt),
        }
    )

    plt.figure(figsize=(12, 10))
    plt.scatter(t_values, data_points - popt[2], label="Norm: L1 with log x axis")

    t_values = np.sort(t_values)
    plt.plot(
        t_values,
        [analyse.exponential(t, *popt) - popt[2] for t in t_values],
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

results.write()
print("Done writing results")
