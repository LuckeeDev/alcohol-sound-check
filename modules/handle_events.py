from enum import Enum
import matplotlib.pyplot as plt

from modules import graphics


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
        self.state = EventsState.FIRST_POINT

    def reset_plot(self):
        plt.clf()
        graphics.plot_and_fit(self.tydelta_tuples)
        plt.show()

    def save_output(self):
        for t, y, y_delta in self.tydelta_tuples:
            self.output_csv.addline(
                {
                    "time": t,
                    "distance": y,
                    "delta_distance": y_delta,
                }
            )

        self.output_csv.write()
        plt.close()

    def __init__(self, tydelta_tuples, output_csv):
        self.tydelta_tuples = tydelta_tuples
        self.output_csv = output_csv

        fig = plt.gcf()
        fig.canvas.mpl_connect("button_press_event", self)
        fig.canvas.mpl_connect("key_press_event", self)
        fig.canvas.mpl_connect("key_release_event", self)

        self.xs = []
        self.ys = []
        self.state = EventsState.FIRST_POINT
        self.ctrl_pressed = False

    def __call__(self, event):
        match event.name:
            case "button_press_event":
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

                        plt.plot(
                            [self.xs[0], self.xs[1]], [self.ys[0], self.ys[0]], "g"
                        )
                        plt.plot(
                            [self.xs[1], self.xs[1]], [self.ys[0], self.ys[1]], "g"
                        )
                        plt.plot(
                            [self.xs[1], self.xs[0]], [self.ys[1], self.ys[1]], "g"
                        )
                        plt.plot(
                            [self.xs[0], self.xs[0]], [self.ys[1], self.ys[0]], "g"
                        )
                        plt.show()

                        self.state = EventsState.FIX
            case "key_press_event":
                match event.key:
                    case "enter":
                        if self.state == EventsState.FIX:
                            self.remove_points()
                            self.state = EventsState.FIRST_POINT
                    case "escape":
                        self.undo_selection()
                        self.state = EventsState.FIRST_POINT
                    case "ctrl+s":
                        self.save_output()
