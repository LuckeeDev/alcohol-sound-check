import numpy as np
from scipy.optimize import curve_fit
from matplotlib.animation import FFMpegWriter, FuncAnimation
import csv
import matplotlib.pyplot as plt
import math

INPUT_FILE = input("Enter the path of the input file: ")
ANIMATION_LENGTH = int(
    input("Enter the length of the animation in seconds (integer): ")
)
FPS = int(input("Enter the frames per second (integer): "))


t_values = []
y_values = []
y_deltas = []

file_name: str

with open(INPUT_FILE, newline="") as file:
    file_name = file.name

    reader = csv.reader(file, delimiter=",")

    first_row_done = False
    for row in reader:
        if first_row_done:
            t_values.append(float(row[0]))
            y_values.append(float(row[1]))
            y_deltas.append(float(row[2]))
        else:
            first_row_done = True

fig = plt.figure(figsize=(10, 8))


def exponential_func(x, a, b, c):
    return a * np.exp(b * x) + c


popt, pcov = curve_fit(
    exponential_func, t_values, y_values, sigma=y_deltas, p0=[20, -1 / 10, 5]
)

plt.scatter(t_values, y_values - popt[2], label="Data")

highest_time = math.ceil(np.max(t_values))
fit_time = np.linspace(0, highest_time, num=highest_time * FPS)
fit_distance = exponential_func(fit_time, popt[0], popt[1], 0)

plt.plot(fit_time, fit_distance, "r-", label="Exponential Fit")
(point,) = plt.plot([], [], "ro")

plt.xlabel("Time (s)")
plt.ylabel("Distance (Hz dB)")
plt.legend()
plt.margins(x=0)
plt.grid(True)


def update(frame):
    x = fit_time[frame]
    y = fit_distance[frame]
    point.set_data([x], [y])
    return (point,)


animation_time = np.min([ANIMATION_LENGTH, highest_time])
frames = animation_time * FPS
ani = FuncAnimation(fig, update, frames=frames, interval=1000 / FPS)

FFwriter = FFMpegWriter(fps=FPS)
animation_file_name = file_name[:-4] + ".mp4"
ani.save(animation_file_name, writer=FFwriter)

print(f"Animation saved as {animation_file_name}")
