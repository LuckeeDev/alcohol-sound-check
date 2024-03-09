import os
import numpy as np
import csv
import scipy.optimize as optimize

from modules.csv_writer import CSVWriter
from modules import utils, analyse

print(
    "Make sure that the output folder is not a subdirectory of the source folder. At most, they can be the same folder."
)
SOURCE_FOLDER = input("Enter the path of the source folder: ")
OUTPUT_FOLDER = input("Enter the path of the output folder: ")
RADIUS = float(
    input(
        "Enter the radius (measured in standard deviations) of the range in which data should be accepted: "
    )
)

utils.ensure_dir(OUTPUT_FOLDER)

for dir_name in utils.list_subdirectories(SOURCE_FOLDER):
    dir_path = os.path.join(SOURCE_FOLDER, dir_name)
    data_path = os.path.join(dir_path, f"{dir_name}.csv")

    t_values = []
    y_values = []
    y_deltas = []

    with open(data_path, newline="") as file:
        reader = csv.reader(file, delimiter=",")

        b = False
        for row in reader:
            if b:
                t_values.append(float(row[0]))
                y_values.append(float(row[1]))
                y_deltas.append(float(row[2]))
            else:
                b = True

    try:
        (par_a, par_b, par_c), pcov = optimize.curve_fit(
            analyse.exponential, t_values, y_values, sigma=y_deltas, p0=[20, -1 / 10, 5]
        )

        delta_a, delta_b, delta_c = np.sqrt(np.diag(pcov))

        t_values_array = np.ndarray(
            shape=(len(t_values)), dtype=float, buffer=np.array(t_values)
        )

        fit_y_values = analyse.exponential(t_values_array, par_a, par_b, par_c)

        errors = analyse.get_error(
            t_values_array, par_a, par_b, delta_a, delta_b, delta_c
        )

        current_output_folder = os.path.join(OUTPUT_FOLDER, dir_name)
        utils.ensure_dir(current_output_folder)
        data_csv_path = os.path.join(current_output_folder, f"{dir_name}.csv")
        data_csv = CSVWriter(data_csv_path, ["time", "distance", "delta_distance"])

        for index in range(len(t_values)):
            if abs(fit_y_values[index] - y_values[index]) < RADIUS * errors[index]:
                data_csv.addline(
                    {
                        "time": t_values_array[index],
                        "distance": y_values[index],
                        "delta_distance": y_deltas[index],
                    }
                )

        data_csv.write()

    except:
        print(f"{dir_name}: fit failed")

    print(f"done {dir_name}")
