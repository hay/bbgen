from bbgen.effects import TimeStretch
from bbgen.util import get_notes_from_track, velocity_to_db
from mido import MidiTrack, MidiFile
from pydub import AudioSegment
import json
import mido

MIDDLE_C:int = 60

class Crapler:
    def __init__(self, segment:AudioSegment, root_note:int = MIDDLE_C):
        self.cache = {}
        self.root_note = root_note
        self.segment = segment

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        length = midi.length
        print(f"Rendering midi file of {length} length, PPQN is {midi.ticks_per_beat}")
        comp = AudioSegment.silent(duration = length * 1000)

        for track in midi.tracks:
            comp = comp.overlay(self._render_track(track, length))

        return comp

    def _render_track(self, track:MidiTrack, length:float) -> AudioSegment:
        data = get_notes_from_track(track)

        if len(data["notes"]) == 0:
            # No notes, skip track
            return AudioSegment.empty()

        comp = AudioSegment.silent(duration = length * 1000)

        for note in data["notes"]:
            semitone = note["note"] - self.root_note
            duration = note["duration"]
            time = note["time"]
            db = velocity_to_db(note["velocity"], 20)

            print(semitone, time, duration, db)

            # Check if the note is in cache
            if semitone in self.cache:
                sample = self.cache[semitone]
            else:
                sample = TimeStretch(pitch = semitone).apply(self.segment)
                self.cache[semitone] = sample

            sample = sample[0:duration].apply_gain(db)
            comp = comp.overlay(sample, position = note["time"])

        return comp