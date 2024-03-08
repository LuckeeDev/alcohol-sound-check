import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import scipy.optimize as optimize

from modules.csv_writer import CSVWriter
from modules import utils, analyse


def func(x, a, b):
    eta, rho, h = x
    return a * eta * h / (rho + b)


print(
    "Make sure that the output folder is not a subdirectory of the source folder. At most, they can be the same folder."
)

SOURCE_FOLDER = input("Enter the path of the source folder: ")
OUTPUT_FOLDER = input("Enter the path of the output folder: ")

utils.ensure_dir(OUTPUT_FOLDER)

results_path = os.path.join(OUTPUT_FOLDER, "fit_results.csv")
fit_results_csv = CSVWriter(
    results_path,
    ["id", "a", "delta_a", "b", "delta_b"],
)

fit_data_path = os.path.join(SOURCE_FOLDER, "fit_data.csv")

t_values = []
t_deltas = []
eta_values = []
eta_deltas = []
rho_values = []
rho_deltas = []
h_values = []
h_deltas = []

with open(fit_data_path, newline="") as file:
    reader = csv.reader(file, delimiter=",")

    b = False
    for row in reader:
        if b:
            t_values.append(float(row[0]))
            t_deltas.append(float(row[1]))
            eta_values.append(float(row[2]))
            eta_deltas.append(float(row[3]))
            rho_values.append(float(row[4]))
            rho_deltas.append(float(row[5]))
            h_values.append(float(row[6]))
            h_deltas.append(float(row[7]))
        else:
            b = True

try:
    (par_a, par_b), pcov = optimize.curve_fit(
        func,
        (eta_values, rho_values, h_values),
        t_values,
        sigma=t_deltas,
        p0=[1, 1],
    )

    print(f"par_a: {par_a}")
    print(f"par_b: {par_b}")
except:
    print("fit failed")
