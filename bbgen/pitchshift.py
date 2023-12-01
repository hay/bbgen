from bbgen.librosaeffect import LibrosaEffect
from dataclasses import dataclass
from pydub import AudioSegment
import librosa

@dataclass
class PitchShift:
    semitones: int = 0

    def apply(self, segment:AudioSegment) -> AudioSegment:
        print(f"Applying pitchshift {self.semitones}")

        effect = LibrosaEffect(segment)

        audio = librosa.effects.pitch_shift(
            effect.data, sr = effect.sample_rate, n_steps = self.semitones
        )

        return effect.process_audio(audio)