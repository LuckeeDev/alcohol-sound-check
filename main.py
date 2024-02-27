import os
from normalise import *
import soundfile as sf

AUDIO_FOLDER = "./audio"

for file_name in os.listdir(AUDIO_FOLDER):
    if file_name.endswith(".wav"):
        file_path = os.path.join(AUDIO_FOLDER, file_name)

        y, sr = librosa.load(file_path, sr=None)
        y_normalised = normalise(y, -3)

        sf.write(file_path, y_normalised, sr)
