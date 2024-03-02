import csv


class CSVWriter:
    def __init__(self, file_path, fields):
        self.file_path = file_path
        self.fields = fields
        self.data = []

    def addline(self, data_dict):
        self.data.append(data_dict)

    def write(self):
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)

            for data_dict in self.data:
                row = [data_dict[key] for key in self.fields]
                writer.writerow(row)
