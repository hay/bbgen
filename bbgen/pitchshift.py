# This is a template for how to build an effect
from dataclasses import dataclass
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import librosa
import soundfile

@dataclass
class PitchShift:
    semitones: int = 0

    def apply(self, segment:AudioSegment) -> AudioSegment:
        print(f"Applying pitchshift {self.semitones}")

        # FIXME: use raw_data instead of the whole song and dance here
        # with tempfiles
        in_file = NamedTemporaryFile()
        out_file = NamedTemporaryFile()

        segment.export(in_file.name, format = "wav")
        data, sample_rate = librosa.load(in_file.name)

        print("Loaded file")

        # Shift pitch
        audio = librosa.effects.pitch_shift(data, sr = sample_rate, n_steps = self.semitones)
        soundfile.write(out_file.name, audio, sample_rate, format = "wav")
        new_segment = AudioSegment.from_wav(out_file.name)

        in_file.close()
        out_file.close()
        return new_segment