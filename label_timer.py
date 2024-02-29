import csv


class LabelTimer:
    labels = {}
    start_time = 0.0

    def __init__(self, path):
        with open(path, newline="") as file:
            reader = csv.reader(file, delimiter="\t")

            for row in reader:
                self.labels[row[2]] = {"begin": float(row[0]), "end": float(row[1])}

        start = self.labels["start"]
        assert start["begin"] == start["end"]
        self.start_time = start["begin"]

    def __call__(self, file_name):
        assert file_name.endswith(".wav")
        label = file_name.removesuffix(".wav")

        label_data = self.labels[label]

        elapsed_time = 0.5 * (label_data["end"] + label_data["begin"]) - self.start_time
        assert elapsed_time > 0

        return elapsed_time
