import librosa
import numpy as np


def normalise(y, peak_db):
    y_db = librosa.power_to_db(y)

    current_peak_db = np.max(y_db)

    scaling_factor = 10 ** ((peak_db - current_peak_db) / 10)

    y_scaled = y * scaling_factor

    return y_scaled
