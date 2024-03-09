import csv
import scipy.optimize as optimize
import numpy as np
from modules import analyse


SOURCE_FILE = input("Enter the path of the CSV file: ")

t_values_index: int = 0
t_deltas_index: int = 0
eta_values_index: int = 0
rho_values_index: int = 0
h_values_index: int = 0

t_values = []
t_deltas = []
eta_values = []
rho_values = []
h_values = []

with open(SOURCE_FILE, newline="") as file:
    reader = csv.reader(file, delimiter=",")

    first_row_done = False

    for row in reader:
        if first_row_done:
            t_values.append(float(row[t_values_index]))
            t_deltas.append(float(row[t_deltas_index]))
            h_values.append(float(row[h_values_index]))
            eta_values.append(float(row[eta_values_index]))
            rho_values.append(float(row[rho_values_index]))
        else:
            t_values_index = row.index("duration")
            t_deltas_index = row.index("delta_duration")
            h_values_index = row.index("height")
            eta_values_index = row.index("viscosity")
            rho_values_index = row.index("density")
            first_row_done = True

data = list(zip(eta_values, rho_values, h_values))

try:
    popt, pcov = optimize.curve_fit(
        analyse.final_fit,
        data,
        t_values,
        sigma=t_deltas,
        p0=[4e5],
    )

    print(f"Parameter a: {popt[0]} +- {np.sqrt(pcov[0, 0])}")
except:
    print("Fit failed")
