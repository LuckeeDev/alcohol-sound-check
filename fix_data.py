import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import scipy.optimize as optimize

from modules.csv_writer import CSVWriter
from modules import utils, analyse

INPUT_PATH = input("Enter the path of the file: ")
OUTPUT_PATH = input("Enter the path of the output folder: ")

results_path = os.path.join(OUTPUT_PATH, "fixed_data.csv")
results_csv = CSVWriter(results_path, ["time", "distance", "delta_distance"])

t_range = []
d_range = []

t_range.append(float(input("from ")))
t_range.append(float(input("to ")))
d_range.append(float(input("from ")))
d_range.append(float(input("to ")))

t_values = []
y_values = []
y_deltas = []

with open(INPUT_PATH, newline="") as file:
    reader = csv.reader(file, delimiter=",")

    b = False
    for row in reader:
        if b:
            t_values.append(float(row[0]))
            y_values.append(float(row[1]))
            y_deltas.append(float(row[2]))
        else:
            b = True

plot_title = analyse.format_plot_title(INPUT_PATH)

fig = plt.figure(figsize=(12, 10))
plt.scatter(t_values, y_values, label="Norm: L1 with log x axis")

max_y = np.max(y_values)
min_y = np.min(y_values)
plt.ylim(top=max_y + 5, bottom=min_y - 5)
plt.xlim(left=0)

try:
    (par_a, par_b, par_c), pcov = optimize.curve_fit(
        analyse.exponential, t_values, y_values, sigma=y_deltas, p0=[20, -1 / 10, 5]
    )

    delta_a, delta_b, delta_c = np.sqrt(np.diag(pcov))

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
except:
    print("fit failed")

plt.legend()

plt.xlabel("Time (s)")
plt.ylabel("Distance (Hz dB)")
plt.title(plot_title)

plt.grid(True)
plt.margins(x=0)


class ClickEvent:
    def __init__(self):
        self.cid = fig.canvas.mpl_connect("button_press_event", self)
        self.xs = []
        self.ys = []
        self.counter = 0

    def __call__(self, event):
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        print(self.xs, self.ys)


click = ClickEvent()

plt.show()


# with open(INPUT_PATH, newline="") as file:
#     reader = csv.reader(file, delimiter=",")

#     b = False
#     for row in reader:
#         if b:
#             if not (
#                 t_range[0] <= float(row[0]) <= t_range[1]
#                 and d_range[0] <= float(row[1]) <= d_range[1]
#             ):
#                 results_csv.addline(
#                     {
#                         "time": row[0],
#                         "distance": row[1],
#                         "delta_distance": row[2],
#                     }
#                 )
#         else:
#             b = True

# results_csv.write()
