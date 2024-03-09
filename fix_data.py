import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.optimize as optimize
from enum import Enum

from modules.csv_writer import CSVWriter
from modules import utils, analyse

mpl.rcParams["toolbar"] = "None"


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

plot_and_fit(tydelta_tuples)


class EventsState(Enum):
    FIRST_POINT = 0
    SECOND_POINT = 1
    FIX = 2


class HandleEvents:
    def remove_points(self):
        min_x = min(self.xs)
        max_x = max(self.xs)
        min_y = min(self.ys)
        max_y = max(self.ys)

        self.tydelta_tuples = [
            (t, y, y_delta)
            for t, y, y_delta in self.tydelta_tuples
            if not (min_x <= t <= max_x and min_y <= y <= max_y)
        ]

        self.reset_plot()

    def undo_selection(self):
        self.reset_plot()
        self.connect_to_button()
        self.state = EventsState.FIRST_POINT

    def reset_plot(self):
        plt.clf()
        plot_and_fit(self.tydelta_tuples)
        plt.show()

    def connect_to_button(self):
        fig = plt.gcf()
        fig.canvas.mpl_disconnect(self.cid)
        self.cid = fig.canvas.mpl_connect("button_press_event", self)

    def connect_to_key(self):
        fig = plt.gcf()
        fig.canvas.mpl_disconnect(self.cid)
        self.cid = fig.canvas.mpl_connect("key_press_event", self)

    def __init__(self, tydelta_tuples):
        fig = plt.gcf()
        self.cid = fig.canvas.mpl_connect("button_press_event", self)
        self.xs = []
        self.ys = []
        self.state = EventsState.FIRST_POINT
        self.tydelta_tuples = tydelta_tuples

    def __call__(self, event):
        match self.state:
            case EventsState.FIRST_POINT:
                self.xs.clear()
                self.ys.clear()
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)

                self.state = EventsState.SECOND_POINT
            case EventsState.SECOND_POINT:
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)

                plt.plot([self.xs[0], self.xs[1]], [self.ys[0], self.ys[0]], "g")
                plt.plot([self.xs[1], self.xs[1]], [self.ys[0], self.ys[1]], "g")
                plt.plot([self.xs[1], self.xs[0]], [self.ys[1], self.ys[1]], "g")
                plt.plot([self.xs[0], self.xs[0]], [self.ys[1], self.ys[0]], "g")
                plt.show()

                self.connect_to_key()
                self.state = EventsState.FIX
            case EventsState.FIX:
                if event.key == "enter":
                    self.remove_points()
                elif event.key == "escape":
                    self.undo_selection()

                self.connect_to_button()
                self.state = EventsState.FIRST_POINT


HandleEvents(tydelta_tuples)

plt.show()
