from bbgen.soundfont import Soundfont
from midi2audio import FluidSynth
from mido import MidiFile, MidiTrack, Message, tempo2bpm
from pathlib import Path
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

def get_notes_from_track(track:MidiTrack) -> list:
    notes = []
    time = 0

    for msg in track:
        time = time + msg.time

        if msg.type == "note_on":
            notes.append({
                "note" : msg.note,
                "velocity" : msg.velocity,
                "time" : time
            })

        if msg.type == "note_off":
            for note in notes:
                if note["note"] == msg.note:
                    note["duration"] = time - note["time"]

    return notes

class Midi:
    def __init__(self, path: Path):
        self.path = path
        self.midi = MidiFile(self.path)

    def get_track(self, track:int):
        return self.midi.tracks[track]

    def render(self, soundfont: Soundfont) -> AudioSegment:
        # Create temp files for in/out files
        in_file = NamedTemporaryFile()
        out_file = NamedTemporaryFile()

        # First write midi data to file
        self.midi.save(in_file.name)

        # Now render
        FluidSynth(soundfont.path).midi_to_audio(in_file.name, out_file.name)

        # Fetch data and return that as a new AudioSegment object
        wave_data = AudioSegment.from_wav(out_file.name)

        # Make sure to close the file handles
        in_file.close()
        out_file.close()

        return wave_data

    def set_program(self, track_index: int, program: int):
        message = Message('program_change', program = program)
        self.midi.tracks[track_index].insert(0, message)
        return self

    @property
    def tracks(self):
        return self.midi.tracks
