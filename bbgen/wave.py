from pathlib import Path
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

class Wave:
    def __init__(self, path: Path = None):
        self.data = None

        if path:
            self.clip = AudioSegment.from_wav(path)

    def as_tmpfile(self):
        file = NamedTemporaryFile(delete = False)
        self.write(file.name)
        return file.name

    def effect(self, effect) -> 'Wave':
        return effect.apply(self)

    @classmethod
    def from_data(cls, data):
        with NamedTemporaryFile() as f:
            f.write(data)
            return cls(f.name)

    def overlay(self, wave:'Wave', position = 0) -> 'Wave':
        self.clip = self.clip.overlay(wave.clip, position)
        return self

    def reverse(self) -> 'Wave':
        self.clip = self.clip.reverse()
        return self

    def write(self, target: str, format: str = "wav"):
        print(f"Writing to {target}")
        self.clip.export(target, format = locals()["format"])