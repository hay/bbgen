from pathlib import Path
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

class Wave:
    def __init__(self, path: Path = None):
        self.data = None

        if path:
            self.clip = AudioSegment.from_wav(path)
        else:
            self.clip = AudioSegment.silent(100)

    def append(self, wave:'Wave', crossfade: int = 100) -> 'Wave':
        self.clip = self.clip.append(wave.clip, crossfade = crossfade)
        return self

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

    @classmethod
    def from_silence(cls, duration:int):
        c = cls()
        c.clip = AudioSegment.silent(duration)
        return c

    def overlay(self, wave:'Wave', position = 0) -> 'Wave':
        self.clip = self.clip.overlay(wave.clip, position)
        return self

    def reverse(self) -> 'Wave':
        self.clip = self.clip.reverse()
        return self

    def write(self, target: str, format: str = "wav"):
        print(f"Writing to {target}")
        self.clip.export(target, format = locals()["format"])