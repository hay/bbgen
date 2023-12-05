from dataclasses import dataclass
from pedalboard import time_stretch
from pedalboard.io import AudioFile
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

@dataclass
class TimeStretch:
    stretch: float = 1
    pitch: float = 0
    high_quality: bool = True

    def apply(self, segment:AudioSegment) -> AudioSegment:
        in_file = NamedTemporaryFile(suffix = ".wav")
        out_file = NamedTemporaryFile(suffix = ".wav")

        segment.export(in_file.name, format = "wav")

        with AudioFile(in_file.name) as inp:
            with AudioFile(out_file.name, 'w', inp.samplerate, inp.num_channels) as out:
                effected = time_stretch(
                    input_audio = inp.read(inp.frames),
                    samplerate = inp.samplerate,
                    stretch_factor = self.stretch,
                    pitch_shift_in_semitones = self.pitch,
                    high_quality = self.high_quality
                )

                out.write(effected)

        new_segment = AudioSegment.from_wav(out_file.name)

        in_file.close()
        out_file.close()

        return new_segment


