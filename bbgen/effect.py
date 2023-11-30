# This is a template for how to build an effect
from bbgen.wave import Wave
from dataclasses import dataclass
from tempfile import NamedTemporaryFile

@dataclass
class Effect:
    value: float = 1.0

    def apply(self, wave:Wave) -> Wave:
        print("Applying effect")
        self._load_wav(wave.as_tmpfile())

        file = NamedTemporaryFile()

        with file:
            self._render(file.name)
            file.seek(0)
            return Wave.from_data(file.read())

        return output