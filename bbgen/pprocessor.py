from dataclasses import dataclass
from loguru import logger
from pedalboard import Pedalboard
from pedalboard.io import AudioFile
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

@dataclass
class PedalboardProcessor:
    board: Pedalboard

    def apply(self, segment:AudioSegment) -> AudioSegment:
        logger.info(f"Applying Pedalboard")

        # FIXME: this must somehow get more efficient
        in_file = NamedTemporaryFile(suffix = ".wav")
        out_file = NamedTemporaryFile(suffix = ".wav")

        segment.export(in_file.name, format = "wav")

        with AudioFile(in_file.name) as inp:
            with AudioFile(out_file.name, 'w', inp.samplerate, inp.num_channels) as out:
                while inp.tell() < inp.frames:
                    chunk = inp.read(inp.samplerate)
                    effected = self.board(chunk, inp.samplerate, reset = False)
                    out.write(effected)

        new_segment = AudioSegment.from_wav(out_file.name)

        in_file.close()
        out_file.close()

        return new_segment