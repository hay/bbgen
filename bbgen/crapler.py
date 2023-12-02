from bbgen.effects import TimeStretch
from mido import MidiTrack
from pydub import AudioSegment

class Crapler:
    def __init__(self, segment:AudioSegment, root_note:int = 60):
        self.segment = segment
        self.root_note = root_note

    def render(self, track:MidiTrack) -> AudioSegment:
        # Middle C = note 60
        time = 0
        messages = []

        for msg in track:
            if msg.type == "note_on":
                print(msg)
                time = time + msg.time
                messages.append({
                    "semitone" : msg.note - self.root_note,
                    "db" : (msg.velocity / 10) - 5, # FIXME
                    "time" : time
                })

        comp = AudioSegment.silent(duration = time)

        for msg in messages:
            note = TimeStretch(pitch = msg["semitone"]).apply(self.segment).apply_gain(msg["db"])
            comp = comp.overlay(note, position = msg["time"])

        return comp