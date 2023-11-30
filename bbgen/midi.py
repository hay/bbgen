from bbgen.soundfont import Soundfont
from bbgen.wave import Wave
from midi2audio import FluidSynth
from mido import MidiFile, MidiTrack, Message
from music21 import converter
from pathlib import Path
from tempfile import NamedTemporaryFile

TINY_NOTATION_PREFIX = "tinyNotation:"

class Midi:
    def __init__(self, path: Path):
        self.path = path
        self.midi = MidiFile(self.path)

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
        # Create temp files for in/out files
        in_file = NamedTemporaryFile()
        out_file = NamedTemporaryFile()

        # First write midi data to file
        self.midi.save(in_file.name)

        # Now render
        FluidSynth(soundfont.path).midi_to_audio(in_file.name, out_file.name)

        # Fetch data and return that as a new Wave object
        out_file.seek(0)
        wave_data = out_file.read()

        # Make sure to close the file handles
        in_file.close()
        out_file.close()

        return Wave.from_data(wave_data)

    def set_program(self, track_index: int, program: int):
        message = Message('program_change', program = program)
        self.midi.tracks[track_index].insert(0, message)
        return self