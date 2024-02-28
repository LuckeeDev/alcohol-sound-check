import librosa
import numpy as np


def get_spectrum(audio_file, sr=None, n_fft=2048, hop_length=None):
    if hop_length is None:
        hop_length = n_fft // 4

    y, sr = librosa.load(audio_file, sr=sr)

    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max(np.abs(D)))

    frequencies = librosa.core.fft_frequencies(sr=sr)
    max_spectrum = np.max(S_db, axis=1)

    return frequencies, max_spectrum


def normalise(y, peak_db):
    y_db = librosa.power_to_db(y)

    current_peak_db = np.max(y_db)

    scaling_factor = 10 ** ((peak_db - current_peak_db) / 10)

    y_scaled = y * scaling_factor

    return y_scaled
