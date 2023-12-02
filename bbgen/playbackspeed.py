from dataclasses import dataclass
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import wave

@dataclass
class Playbackspeed:
    rate: float = 1

    def apply(self, segment:AudioSegment) -> AudioSegment:
        print(f"Applying Playbackspeed {self.rate}")

        # FIXME: this must somehow get more efficient
        in_file = NamedTemporaryFile()
        out_file = NamedTemporaryFile()

        segment.export(in_file.name, format = "wav")

        inp = wave.open(in_file.name, "rb")
        out = wave.open(out_file.name, "wb")

        signal = inp.readframes(-1)
        out.setnchannels(segment.channels)
        out.setsampwidth(segment.sample_width)
        out.setframerate(segment.frame_rate * self.rate)
        out.writeframes(signal)

        segment = AudioSegment.from_wav(out_file.name)

        in_file.close()
        out_file.close()
        inp.close()
        out.close()

        return segment