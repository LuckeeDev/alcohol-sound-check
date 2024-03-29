import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import scipy.optimize as optimize

from modules.csv_writer import CSVWriter
from modules import utils, analyse

# Enable LaTeX
plt.rcParams.update({"text.usetex": True, "font.size": 20})

print(
    "Make sure that the output folder is not a subdirectory of the source folder. At most, they can be the same folder."
)
SOURCE_FOLDER = input("Enter the path of the source folder: ")
OUTPUT_FOLDER = input("Enter the path of the output folder: ")

utils.ensure_dir(OUTPUT_FOLDER)

results_path = os.path.join(OUTPUT_FOLDER, "results_fixed.csv")
results_csv = CSVWriter(
    results_path,
    ["id", "duration", "delta_duration"],
)

for dir_name in utils.list_subdirectories(SOURCE_FOLDER):
    dir_path = os.path.join(SOURCE_FOLDER, dir_name)

    invalid_path = os.path.join(dir_path, "INVALID")

    if os.path.exists(invalid_path) and os.path.isfile(invalid_path):
        print(f"Skipping {dir_name} because it is marked as invalid")
        continue

    data_path = os.path.join(dir_path, "fixed_data.csv")

    t_values = []
    y_values = []
    y_deltas = []

    with open(data_path, newline="") as file:
        reader = csv.reader(file, delimiter=",")

        first_row_done = False
        for row in reader:
            if first_row_done:
                t_values.append(float(row[0]))
                y_values.append(float(row[1]))
                y_deltas.append(float(row[2]))
            else:
                first_row_done = True

    plot_title = analyse.format_plot_title(dir_name)

    plt.figure(figsize=(12, 10))

    current_output_folder = os.path.join(OUTPUT_FOLDER, dir_name)
    utils.ensure_dir(current_output_folder)

    log_file_path = os.path.join(current_output_folder, f"{dir_name}_fixed_log.txt")

    try:
        (par_a, par_b, par_c), pcov = optimize.curve_fit(
            analyse.exponential, t_values, y_values, sigma=y_deltas, p0=[20, -1 / 10, 5]
        )

        delta_a, delta_b, delta_c = np.sqrt(np.diag(pcov))

        results_csv.addline(
            {
                "id": dir_name,
                "duration": -1 / par_b,
                "delta_duration": delta_b / par_b**2,
            }
        )

        y_values = y_values - par_c
        plt.scatter(t_values, y_values, label="Distance")

        t0 = 0
        tf = np.max(t_values)
        t_values = np.linspace(t0, tf, 10000)
        y_values = analyse.exponential(t_values, par_a, par_b, 0)
        plt.plot(
            t_values,
            y_values,
            "r",
            label=f"Exponential fit ($\\tau = {-1/par_b:.2f} \\pm {delta_b/par_b**2:.2f}$ s)",
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

    fig_path = os.path.join(OUTPUT_FOLDER, dir_name, f"{dir_name}_fixed.pdf")
    plt.savefig(fig_path)
    plt.close()

    print(f"Done {plot_title}")

results_csv.write()
print("Done writing results")
