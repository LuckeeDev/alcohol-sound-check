import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

from modules import analyse


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

    plt.grid(True)
    plt.margins(x=0)
