import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from bbgen.isobar import Timeline
from bbgen.pprocessor import PedalboardProcessor
from mido import MidiFile
from pedalboard import Pedalboard, Delay, Reverb
import isobar as iso
import random

# add random with seed
episodeSeed = 10 # @param {type:"integer"}
random.seed(episodeSeed)

# simpele sequentie
#chord_sequence = [7, 4, 5, 2] # @param {type:"raw"}
chord_sequence = random.sample(range(0, 8), 4)

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
workerSeed = 1 # @param {type:"integer"}
random.seed(workerSeed)
possible_keys = [['C#', 'minor'], ['A', 'major'], ['G#', 'minor']]
picked_key = random.choice(possible_keys)
note_names = picked_key[0]
key_types = picked_key[1]
key_sequence = iso.Key(note_names, key_types)
print(key_sequence)

chord_sequence_iso = iso.PSequence([(notesInChord[0]+element,notesInChord[1]+element,notesInChord[2]+element) for element in chord_sequence])

durationChords = 16

key = iso.PStaticPattern(key_sequence, 4)
timeline = Timeline(60)
timeline.schedule({
    "degree": chord_sequence_iso,
    "key": key,
    "octave": 3,
    "duration": durationChords,
    "amplitude": 25,
})

instrument = Dreamstrument(
    path = "sounds/instruments/voices/essentialWorkers-pad1",
    round_robin = True,
)

# midi = timeline.to_midi()
# midi.save("synth-test.mid")
midi = MidiFile("./synth-test.mid")
comp = instrument.render_midi(midi)

board = Pedalboard([
    Delay(0.5, feedback = 0.5, mix = 0.3),
    Reverb(room_size=0.7, wet_level = 0.5, dry_level = 0.5)
])

comp2 = PedalboardProcessor(board).apply(comp)
comp2.export("output/synthTest.mp3")