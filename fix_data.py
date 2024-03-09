import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

from modules.csv_writer import CSVWriter
from modules.handle_events import HandleEvents
from modules import utils, graphics

mpl.rcParams["toolbar"] = "None"


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

graphics.plot_and_fit(tydelta_tuples)

HandleEvents(tydelta_tuples, output_csv)

plt.show()
