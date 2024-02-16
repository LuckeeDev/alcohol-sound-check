import librosa
import sounddevice as sd


def process_audio_file(file_path: str, threshold: float):
    audio, sr = librosa.load(file_path, sr=None)  # Load the audio file
    audio_abs = abs(audio)  # Take the absolute values of the audio samples

    # Play the audio file
    sd.play(audio, sr)

    for i in range(len(audio_abs)):
        print(audio_abs[i])
        # if audio_abs[i] >= threshold:
        #     print(f"Threshold reached at sample {i}!")

    # Wait for the audio file to finish playing
    sd.wait()


# Example usage
file_path = "test.wav"
threshold = 0.5  # Adjust the threshold value as per your requirement

process_audio_file(file_path, threshold)
