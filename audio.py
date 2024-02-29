import librosa
import numpy as np


def get_spectrum(audio_data, sr, n_fft=2048, hop_length=None):
    if hop_length is None:
        hop_length = n_fft // 4

    D = librosa.stft(audio_data, n_fft=n_fft, hop_length=hop_length)

    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max(np.abs(D)))

    frequencies = librosa.core.fft_frequencies(sr=sr)
    max_spectrum = np.max(S_db, axis=1)

    return frequencies, max_spectrum
