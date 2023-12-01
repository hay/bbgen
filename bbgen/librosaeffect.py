from dataclasses import dataclass
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import librosa
import soundfile

class LibrosaEffect:
    def __init__(self, segment:AudioSegment):
        # FIXME: use raw_data instead of the whole song and dance here
        # with tempfiles
        self.in_file = NamedTemporaryFile()
        self.out_file = NamedTemporaryFile()

        segment.export(self.in_file.name, format = "wav")
        self.data, self.sample_rate = librosa.load(self.in_file.name)

    def process_audio(self, audio) -> AudioSegment:
        soundfile.write(self.out_file.name, audio, self.sample_rate, format = "wav")
        new_segment = AudioSegment.from_wav(self.out_file.name)

        self.in_file.close()
        self.out_file.close()
        return new_segment