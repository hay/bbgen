# This is a template for how to build an effect
from bbgen.wave import Wave
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
import librosa
import soundfile

@dataclass
class PitchShift:
    semitones: int = 0

    def apply(self, wave:Wave) -> Wave:
        print(f"Applying pitchshift {self.semitones}")

        data, sample_rate = librosa.load(wave.as_tmpfile())

        print("Loaded file")

        # Shift pitch
        audio = librosa.effects.pitch_shift(data, sr = sample_rate, n_steps = self.semitones)

        # Save
        file = NamedTemporaryFile()

        with file:
            soundfile.write(file.name, audio, sample_rate, format = "wav")
            file.seek(0)
            return Wave.from_data(file.read())

        return output