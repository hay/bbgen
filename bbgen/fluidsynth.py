from midi2audio import FluidSynth as fs
from mido import MidiFile
from pathlib import Path
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

class FluidSynth:
    def __init__(self, soundfont_path: Path):
        self.soundfont_path = soundfont_path

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create temp files for in/out files
        in_file = NamedTemporaryFile()
        out_file = NamedTemporaryFile()

        # First write midi data to file
        midi.save(in_file.name)

        # Now render
        fs(self.soundfont_path).midi_to_audio(in_file.name, out_file.name)

        # Fetch data and return that as a new AudioSegment object
        wave_data = AudioSegment.from_wav(out_file.name)

        # Make sure to close the file handles
        in_file.close()
        out_file.close()

        return wave_data