from bbgen.librosaeffect import LibrosaEffect
from dataclasses import dataclass
from pydub import AudioSegment
import librosa

@dataclass
class TimeStretch:
    rate: float = 1

    def apply(self, segment:AudioSegment) -> AudioSegment:
        print(f"Applying TimeStretch {self.rate}")

        effect = LibrosaEffect(segment)

        audio = librosa.effects.time_stretch(
            effect.data, rate = self.rate
        )

        return effect.process_audio(audio)