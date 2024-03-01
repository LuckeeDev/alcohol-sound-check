import csv


class ResultsWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def addline(self, data_dict):
        self.data.append(data_dict)

    def write(self):
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "norm_id", "duration", "intensity"])
            for data_dict in self.data:
                writer.writerow(
                    [
                        data_dict["id"],
                        data_dict["norm_id"],
                        data_dict["duration"],
                        data_dict["intensity"],
                    ]
                )
