# base chord loop is created using an episode seed (for the akkoordtrap)
# and the workerseed (Anniek, Lex, Ruben)- 0,1,2. these determine the scale.
# NOTE: this is now only used for intro tune
import sys
sys.path.append("..")


from bbgen.isobar import Timeline
from IPython.display import Audio
import isobar as iso
from pydub import AudioSegment
from bbgen.dreampler import Dreampler
from bbgen.dreamstrument import Dreamstrument
from bbgen.effects import PedalboardProcessor, Playbackspeed, TimeStretch
from pedalboard import Pedalboard, Chorus, Reverb, Phaser, Delay, Gain
from mido import MidiFile
from bbgen.fluidsynth import FluidSynth
from bbgen.util import set_midi_program_for_track
import random

# add random with seed
worker = "Lex" #@param ["Lex", "Anniek", "Ruben"]
workerSeed = 0
if worker == "Anniek":
  workerSeed = 1
elif worker == "Ruben":
  workerSeed = 2

x_minutes = 1 # @param {type:"slider", min:0, max:10, step:0.1}

# make jingle for beginning (& end???)


# simpele sequentie
#chord_sequence = [7, 4, 5, 2] # @param {type:"raw"}
chord_sequence = random.sample(range(0, 8), 4)

durationChords = 16

# noten om te spelen
notesInChord = [0, 2, 4]
# Possible values to add or subtract
values = [0, 7, 12]

# Generate the new list
new_notes = []
for note in notesInChord:
    value_to_add_or_subtract = random.choice(values)
    add_or_subtract = random.choice([1, -1])
    new_note = note + (value_to_add_or_subtract * add_or_subtract)
    new_notes.append(new_note)

notesInChord = new_notes


# zero based
chord_sequence = [element - 1 for element in chord_sequence]

# toonladder gebaseerd op welke worker
workerNumber = workerSeed
possible_keys = [['C#', 'minor'], ['A', 'major'], ['G#', 'minor']]
picked_key = possible_keys[workerNumber]
note_names = picked_key[0]
key_types = picked_key[1]
key_sequence = iso.Key(note_names, key_types)

timeline = Timeline(durationChords*len(chord_sequence)/4)

noteList = [0, 3, 7, 9] + ([None] * 32) + [9, 7, 3,0] + ([None] * 32) + ([None] * 32)

timeline.schedule({
    "degree": iso.PSequence(noteList),
    "key": key_sequence,
    "octave": 2,
    "duration": durationChords/64,
    "amplitude": 127,
})

instrument = Dreamstrument(
    path = "sounds-mark/instruments/voices/essentialWorkers-lead1",
    round_robin = True
)

midi = timeline.to_midi()
compJingle = instrument.render_midi(midi).normalize()

compJingle.export("output/jingle.mp3")