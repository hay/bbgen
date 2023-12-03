from bbgen.effects import TimeStretch
from mido import MidiTrack, MidiFile
from pydub import AudioSegment

MIDDLE_C:int = 60

class Crapler:
    def __init__(self, segment:AudioSegment, root_note:int = MIDDLE_C):
        self.cache = {}
        self.root_note = root_note
        self.segment = segment

    def render_midi(self, file:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        print(f"Rendering midi file of {file.midi.length} length")
        comp = AudioSegment.silent(duration = file.midi.length * 1000)

        # First render the first track, then just loop over the rest
        for track in file.tracks:
            comp = comp.overlay(self.render_track(track))

        return comp

    def render_track(self, track:MidiTrack) -> AudioSegment:
        time = 0
        messages = []

        for msg in track:
            if msg.type == "note_on":
                print(msg)
                time = time + msg.time
                messages.append({
                    "semitone" : msg.note - self.root_note,
                    "db" : -(msg.velocity / 10) - 3, # FIXME
                    "time" : time
                })

        comp = AudioSegment.silent(duration = time)

        for msg in messages:
            # Adding a cache, this makes rendering four times as fast
            nid = str(msg["semitone"]) + ":" + str(msg["db"])
            print(nid)

            if nid in self.cache:
                note = self.cache[nid]
            else:
                note = TimeStretch(pitch = msg["semitone"]).apply(self.segment).apply_gain(msg["db"])
                self.cache[nid] = note

            comp = comp.overlay(note, position = msg["time"])

        return comp