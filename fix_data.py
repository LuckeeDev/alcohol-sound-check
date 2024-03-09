import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import scipy.optimize as optimize

from modules.csv_writer import CSVWriter
from modules import utils, analyse


def plot_and_fit(tydelta_tuples):
    t_values, y_values, y_deltas = list(zip(*tydelta_tuples))

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
        print("Fit failed")

    plt.legend()

    plt.xlabel("Time (s)")
    plt.ylabel("Distance (Hz dB)")
    plt.title(INPUT_FILE)

    plt.grid(True)
    plt.margins(x=0)


print(
    'INPUT FILE NAME SHOULD NOT BE "fixed_data.csv". YOU CANNOT UNDO WHAT THIS SCRIPT DOES.'
)
INPUT_FILE = input("Enter the path of the input file: ")
OUTPUT_PATH = input("Enter the path of the output folder: ")
utils.ensure_dir(OUTPUT_PATH)

output_file_path = os.path.join(OUTPUT_PATH, "fixed_data.csv")
output_csv = CSVWriter(output_file_path, ["time", "distance", "delta_distance"])

tydelta_tuples = []

with open(INPUT_FILE, newline="") as file:
    reader = csv.reader(file, delimiter=",")

    first_row_done = False
    for row in reader:
        if first_row_done:
            tydelta_tuples.append((float(row[0]), float(row[1]), float(row[2])))
        else:
            first_row_done = True

fig, ax = plt.subplots()
fig.set_figwidth(12)
fig.set_figheight(10)

plot_and_fit(tydelta_tuples)


class HandleEvents:
    def enter(self):
        min_x = min(self.xs)
        max_x = max(self.xs)
        min_y = min(self.ys)
        max_y = max(self.ys)

        self.tydelta_tuples = [
            (t, y, y_delta)
            for t, y, y_delta in self.tydelta_tuples
            if not (min_x <= t <= max_x and min_y <= y <= max_y)
        ]

        plt.clf()
        plot_and_fit(self.tydelta_tuples)
        plt.show()

    def esc(self):
        fig.canvas.mpl_disconnect(self.cid)
        fig.canvas.mpl_connect("button_press_event", self)
        self.counter = 0

    def __init__(self, tydelta_tuples):
        self.cid = fig.canvas.mpl_connect("button_press_event", self)
        self.xs = []
        self.ys = []
        self.counter = 0
        self.tydelta_tuples = tydelta_tuples

    def __call__(self, event):
        if self.counter == 0:
            self.xs.clear()
            self.ys.clear()
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.counter += 1
        elif self.counter == 1:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)

            (line_1,) = ax.plot([self.xs[0], self.xs[1]], [self.ys[0], self.ys[0]], "g")
            line_1.figure.canvas.draw()

            (line_2,) = ax.plot([self.xs[1], self.xs[1]], [self.ys[0], self.ys[1]], "g")
            line_2.figure.canvas.draw()

            (line_3,) = ax.plot([self.xs[1], self.xs[0]], [self.ys[1], self.ys[1]], "g")
            line_3.figure.canvas.draw()

            (line_4,) = ax.plot([self.xs[0], self.xs[0]], [self.ys[1], self.ys[0]], "g")
            line_4.figure.canvas.draw()

            fig.canvas.mpl_disconnect(self.cid)
            self.cid = fig.canvas.mpl_connect("key_press_event", self)

            self.counter += 1
        elif self.counter == 2:
            if event.key == "enter":
                print("Enter event captured")
                self.enter()
            elif event.key == "escape":
                self.esc()


HandleEvents(tydelta_tuples)

plt.show()
