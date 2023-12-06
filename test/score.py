import sys
sys.path.append("..")

from bbgen.fluidsynth import FluidSynth
from dataclasses import dataclass
from isobar.util import note_name_to_midi_note
from mido import MetaMessage, Message, MidiFile, MidiTrack
import mido
import re

birthday = "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"

song = """
G3(0,0,0.5) G3(1.2,0.3,0.8) A3(2.4,0.3,0.8) G3(3.6,0.3,0.8) C4(4.8,0.3,0.8) B3(6,0.3,0.8)
G3(7.2,0.3,0.8) G3(8.4,0.3,0.8) A3(9.6,0.3,0.8) G3(10.8,0.3,0.8) D4(12,0.3,0.8) C4(13.2,0.3,0.8)
G3(14.4,0.3,0.8) G3(15.6,0.3,0.8) G4(16.8,0.3,0.8) E4(18,0.3,0.8) C4(19.2,0.3,0.8) B3(20.4,0.3,0.8) A3(21.6,0.3,0.8)
F4(22.8,0.3,0.8) F4(24,0.3,0.8) E4(25.2,0.3,0.8) C4(26.4,0.3,0.8) D4(27.6,0.3,0.8) C4(28.8,0.3,0.8)
"""

jazzy = """
C4(0,0,0.7) G3(1,0.2,0.6) G3(2,0.2,0.6) A3(3,0.2,0.7) G3(4,0.2,0.6) F3(5,0.2,0.6) E3(6,0.2,0.7)
C4(7,0.2,0.7) G3(8,0.2,0.6) G3(9,0.2,0.6) A3(10,0.2,0.7) G3(11,0.2,0.6) D4(12,0.2,0.7) C4(13,0.2,0.7)
"""

RE_PATTERN = re.compile(r'([^(\s]+)\(([^)]*)\)')

class Note:
    def __init__(self, note:str):
        match = RE_PATTERN.findall(note)[0]
        macro, arguments = match
        args = [float(a) for a in arguments.split(",")]
        self.note = macro
        self.time = args[0]
        self.duration = args[1]
        self.velocity = args[2]


class BBScore:
    def __init__(self, score:str, bpm:int = 120, ticks_per_beat:int = 480):
        self.bpm = bpm
        self.score = score
        self.ticks_per_beat = ticks_per_beat
        self._notes = score.strip().split(" ")
        self._tempo = int(60000000 / self.bpm)


    def notes(self):
        yield MetaMessage('set_tempo', tempo = self._tempo, time = 0)
        yield MetaMessage('time_signature',
            numerator = 4,
            denominator = 4,
            clocks_per_click = 24,
            notated_32nd_notes_per_beat = 8,
            time = 0
        )

        time = 0
        for n in self._notes:
            note = Note(n)
            note_int = note_name_to_midi_note(note.note)

            if note.duration == 0:
                continue

            on_time = int(self.ticks_per_beat / (note.time - time))
            off_time = int(self.ticks_per_beat / note.duration)
            time = note.time + note.duration
            velocity = int(note.velocity * 127)

            yield Message("note_on", note = note_int, velocity = velocity, time = on_time)
            yield Message("note_off", note = note_int, velocity = velocity, time = off_time)

midi = MidiFile(ticks_per_beat = 960)
track = MidiTrack()
midi.tracks.append(track)

for note in BBScore(jazzy, bpm = 480).notes():
    print(note)
    track.append(note)

midi.save("output/score.mid")

FluidSynth("./FluidR3Mono_GM.sf3").render_midi(midi).export("output/score.mp3")