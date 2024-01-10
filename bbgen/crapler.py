from bbgen.effects import TimeStretch
from bbgen.util import get_notes_from_midi, velocity_to_db
from mido import MidiTrack, MidiFile
from pydub import AudioSegment
import json
import mido

MIDDLE_C:int = 60

class Crapler:
    def __init__(self, segment:AudioSegment, root_note:int = MIDDLE_C):
        if not isinstance(segment, AudioSegment):
            raise Exception(f"Segment is not an AudioSegment but {type(segment)}: {segment}")

        self.cache = {}
        self.root_note = root_note
        self.segment = segment

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        length = midi.length
        print(f"Rendering midi file of {length} length, PPQN is {midi.ticks_per_beat}")
        comp = AudioSegment.silent(duration = length * 1000)

        for note in get_notes_from_midi(midi):
            semitone = note["note"] - self.root_note
            duration = note["duration"]
            time = note["time"]
            db = velocity_to_db(note["velocity"], 20)

            # Check if the note is in cache
            if semitone in self.cache:
                sample = self.cache[semitone]
            else:
                sample = TimeStretch(pitch = semitone).apply(self.segment)
                self.cache[semitone] = sample

            sample = sample[0:duration * 1000].apply_gain(db)
            comp = comp.overlay(sample, position = time * 1000)

        return comp