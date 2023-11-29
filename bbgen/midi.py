from bbgen.soundfont import Soundfont
from bbgen.wave import Wave
from midi2audio import FluidSynth
from music21 import converter
from pathlib import Path
from tempfile import NamedTemporaryFile

TINY_NOTATION_PREFIX = "tinyNotation:"

class Midi:
    def __init__(self, path: Path):
        self.path = path

    # Render Tinynotation as a new MIDI file
    @classmethod
    def from_tinynotation(cls, notation:str):
        notation = notation.strip()

        # Check if we have the "tinyNotation:" prefix and otherwise add it
        if notation.find(TINY_NOTATION_PREFIX) != 0:
            notation = TINY_NOTATION_PREFIX + notation

        with NamedTemporaryFile(delete = False) as file:
            score = converter.parse(notation)
            score.write("midi", fp = file.name)
            return cls(file.name)

    def render(self, soundfont: Soundfont) -> Wave:
        with NamedTemporaryFile() as file:
            FluidSynth(soundfont.path).midi_to_audio(self.path, file.name)
            file.seek(0)
            return Wave.from_data(file.read())