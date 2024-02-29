import csv


class LabelReader:
    begin_list = []
    end_list = []
    label_list = []
    start_time = 0.0

    def __init__(self):
        with open("labels.txt", newline="") as file:
            reader = csv.reader(file, delimiter="\t")

            for row in reader:
                self.begin_list.append(float(row[0]))
                self.end_list.append(float(row[1]))
                self.label_list.append(row[2])

        start_index = self.label_list.index("start")
        assert self.begin_list[start_index] == self.end_list[start_index]
        self.start_time = self.begin_list[start_index]

    def elapsed_time(self, file_name):
        assert file_name.endswith(".wav")
        label = file_name.removesuffix(".wav")

        index = self.label_list.index(label)

        elapsed_time = (
            0.5 * (self.end_list[index] + self.begin_list[index]) - self.start_time
        )
        assert elapsed_time > 0

        return elapsed_time
