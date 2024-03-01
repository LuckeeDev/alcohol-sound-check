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
OUTPUT_FOLDER = input("Enter the path of the output folder: ")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

LABELS_FILE_NAME = "labels.txt"

results = ResultsWriter(os.path.join(OUTPUT_FOLDER, "results.csv"))


for dir_name in os.listdir(AUDIO_FOLDER):
    dir_path = os.path.join(AUDIO_FOLDER, dir_name)

    labels_file_path = os.path.join(dir_path, LABELS_FILE_NAME)
    timer = LabelTimer(labels_file_path)

    references = []
    reference_folder_path = os.path.join(dir_path, "reference")

    for file_name in os.listdir(reference_folder_path):
        file_path = os.path.join(reference_folder_path, file_name)
        y, sr = librosa.load(file_path, sr=None)

        frequencies, spectrum = audio.get_spectrum(y, sr)
        references.append((frequencies, spectrum))

    t_values = []
    data_points = []
    effect_folder = os.path.join(dir_path, "effect")

    for file_name in os.listdir(effect_folder):
        t_values.append(timer(file_name))

        file_path = os.path.join(effect_folder, file_name)
        y, sr = librosa.load(file_path, sr=None)

        frequencies, spectrum = audio.get_spectrum(y, sr)

        distance = analyse.get_distance(norms.l1_log, spectrum, references, frequencies)
        data_points.append(distance)

    plot_title = analyse.format_plot_title(dir_name)
    popt = None

    try:
        popt, _ = optimize.curve_fit(
            analyse.exponential, t_values, data_points, p0=[20, -1 / 10, 5]
        )

        results.addline(
            {
                "id": dir_name,
                "norm_id": "l1_log",
                "duration": -1 / popt[1],
                "intensity": analyse.exponential(0, *popt),
            }
        )

        data_points = data_points - popt[2]
    except:
        print(f"Fit failed: {plot_title}")

    plt.figure(figsize=(12, 10))
    plt.scatter(t_values, data_points, label="Norm: L1 with log x axis")

    if popt is not None:
        t0 = 0
        tf = np.max(t_values)
        t_values = np.linspace(t0, tf, 10000)

        plt.plot(
            t_values,
            [analyse.exponential(t, *popt) - popt[2] for t in t_values],
            "r",
            label="Fit",
        )
    plt.legend()

    plt.xlabel("Time (s)")
    plt.ylabel("Distance")
    plt.title(plot_title)

    plt.grid(True)
    plt.margins(x=0)
    plt.xlim(left=0)

    fig_path = os.path.join(OUTPUT_FOLDER, f"{dir_name}.pdf")
    plt.savefig(fig_path)
    plt.close()

    print(f"Done {plot_title}")

results.write()
print("Done writing results")
