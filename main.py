import os
from normalise import *
import soundfile as sf
import matplotlib.pyplot as plt
import librosa
from scipy.interpolate import interp1d
from scipy.integrate import quad, simpson

# AUDIO_FOLDER = "./audio"

# for file_name in os.listdir(AUDIO_FOLDER):
#     if file_name.endswith(".wav"):
#         file_path = os.path.join(AUDIO_FOLDER, file_name)

#         y, sr = librosa.load(file_path, sr=None)
#         y_normalised = normalise(y, -3)

#         sf.write(file_path, y_normalised, sr)


# Function to compute maximum spectrum
def compute_max_spectrum(audio_file, sr=None):
    # Load audio file
    y, sr = librosa.load(audio_file, sr=sr)

    # Compute STFT
    D = librosa.stft(y)

    # Convert magnitude spectrogram to decibels (dB)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max(np.abs(D)))

    # Find maximum spectrum (maximum amplitude across time)
    max_spectrum = np.max(S_db, axis=1)
    frequencies = librosa.core.fft_frequencies(sr=sr)

    return max_spectrum, sr, frequencies


# Function to interpolate the maximum spectrum
def interpolate_spectrum(max_spectrum, sr):
    # Generate frequency axis
    freqs = librosa.core.fft_frequencies(sr=sr)

    # Perform cubic interpolation
    f_interp = interp1d(freqs, max_spectrum, kind="cubic")

    # New frequency axis (more points for smoother interpolation)
    freqs_interp = np.linspace(freqs.min(), freqs.max(), num=1000)

    # Interpolate the spectrum
    max_spectrum_interp = f_interp(freqs_interp)

    return max_spectrum_interp, freqs_interp, f_interp


# Function to plot interpolated spectrum
def plot_interpolated_spectrum(max_spectrum_interp, freqs_interp):
    # Plot interpolated spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(freqs_interp, max_spectrum_interp)
    plt.title("Interpolated Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xscale("log")
    plt.xlim(100, 16000)
    plt.grid(True, which="both", ls="--")
    plt.show()


audio_file1 = "audio/reference-01.wav"
audio_file2 = "audio/reference-02.wav"
max_spectrum1, sr, freqs1 = compute_max_spectrum(audio_file1)
max_spectrum2, sr, freqs2 = compute_max_spectrum(audio_file2)
msi1, freq1, func1 = interpolate_spectrum(max_spectrum1, sr)
msi2, freq2, func2 = interpolate_spectrum(max_spectrum2, sr)
plot_interpolated_spectrum(msi1, freq1)
plot_interpolated_spectrum(msi2, freq2)

# print(func1(1000))

print(quad(lambda x: np.abs(func1(x) - func2(x)) / np.log10(x), 100, 16000))
print(simpson(np.abs(max_spectrum1[1:] - max_spectrum2[1:]), x=np.log10(freqs1[1:])))
