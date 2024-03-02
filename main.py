import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.optimize as optimize
import librosa

from modules import audio, analyse, norms, utils
from modules.csv_writer import CSVWriter
from modules.label_timer import LabelTimer

from modules.constants import LABELS_FILE_NAME

print(
    "Make sure that the output folder is not a subdirectory of the audio folder. At most, they can be the same folder."
)
AUDIO_FOLDER = input("Enter the path of the audio folder: ")
OUTPUT_FOLDER = input("Enter the path of the output folder: ")

utils.ensure_dir(OUTPUT_FOLDER)

results_path = os.path.join(OUTPUT_FOLDER, "results.csv")
results_csv = CSVWriter(
    results_path,
    ["id", "norm_id", "duration", "delta_duration", "intensity", "delta_intensity"],
)

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

    plt.figure(figsize=(12, 10))
    plt.scatter(t_values, data_points, label="Norm: L1 with log x axis")

    max_y = np.max(data_points)
    min_y = np.min(data_points)
    plt.ylim(top=max_y + 5, bottom=min_y - 5)
    plt.xlim(left=0)

    current_output_folder = os.path.join(OUTPUT_FOLDER, dir_name)
    utils.ensure_dir(current_output_folder)
    data_csv_path = os.path.join(current_output_folder, f"{dir_name}.csv")
    data_csv = CSVWriter(data_csv_path, ["time", "distance"])

    for index in range(len(t_values)):
        data_csv.addline({"time": t_values[index], "distance": data_points[index]})

    data_csv.write()

    log_file_path = os.path.join(current_output_folder, f"{dir_name}_log.txt")

    try:
        (par_a, par_b, par_c), pcov = optimize.curve_fit(
            analyse.exponential, t_values, data_points, p0=[20, -1 / 10, 5]
        )

        delta_a, delta_b, delta_c = np.sqrt(np.diag(pcov))

        results_csv.addline(
            {
                "id": dir_name,
                "norm_id": "l1_log",
                "duration": -1 / par_b,
                "delta_duration": delta_b / par_b**2,
                "intensity": par_a,
                "delta_intensity": delta_a,
            }
        )

        t0 = 0
        tf = np.max(t_values)
        t_values = np.linspace(t0, tf, 10000)
        y_values = analyse.exponential(t_values, par_a, par_b, par_c)

        plt.plot(
            t_values,
            y_values,
            "r",
            label="Fit",
        )

        errors = analyse.get_error(t_values, par_a, par_b, delta_a, delta_b, delta_c)
        plt.fill_between(
            t_values,
            y_values - errors,
            y_values + errors,
            color="r",
            alpha=0.2,
            label="Error",
        )

        with open(log_file_path, "w") as log_file:
            log_file.write(f"Parameter a: {par_a} +- {delta_a}\n")
            log_file.write(f"Parameter b: {par_b} +- {delta_b}\n")
            log_file.write(f"Parameter c: {par_c} +- {delta_c}\n")
    except:
        with open(log_file_path, "w") as log_file:
            log_file.write(f"Fit failed")

    plt.legend()

    plt.xlabel("Time (s)")
    plt.ylabel("Distance (Hz dB)")
    plt.title(plot_title)

    plt.grid(True)
    plt.margins(x=0)

    fig_path = os.path.join(OUTPUT_FOLDER, dir_name, f"{dir_name}.pdf")
    plt.savefig(fig_path)
    plt.close()

    print(f"Done {plot_title}")

results_csv.write()
print("Done writing results")
