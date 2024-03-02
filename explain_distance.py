import librosa
import audio
import matplotlib.pyplot as plt

EFFECT_PATH = input("Enter the path of the effect audio file: ")
REFERENCE_PATH = input("Enter the path of the reference audio file: ")
OUTPUT_PATH = "explain_distance.pdf"

y_effect, sr_effect = librosa.load(EFFECT_PATH, sr=None)
effect_frequencies, effect_spectrum = audio.get_spectrum(y_effect, sr_effect)

y_reference, sr_reference = librosa.load(REFERENCE_PATH, sr=None)
reference_frequencies, reference_spectrum = audio.get_spectrum(
    y_reference, sr_reference
)


plt.figure(figsize=(10, 6))
plt.xscale("log")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("Spectral distance")

plt.tight_layout()
plt.margins(x=0)
plt.xlim(right=18000)

plt.plot(effect_frequencies, effect_spectrum, label="Effect")
plt.plot(reference_frequencies, reference_spectrum, label="Reference")
plt.fill_between(
    reference_frequencies,
    reference_spectrum,
    effect_spectrum,
    alpha=0.5,
    label="Distance",
)

plt.legend()
plt.savefig(OUTPUT_PATH)
plt.close()
