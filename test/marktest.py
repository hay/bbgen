import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from bbgen.isobar import Timeline
import isobar as iso
import random

possible_keys = [['C#', 'minor'], ['A', 'major'], ['G#', 'minor']]
picked_key = random.choice(possible_keys)
note_names = picked_key[0]
key_types = picked_key[1]
key_sequence = iso.Key(note_names, key_types)
durationChords = 16

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
chord_sequence_iso = iso.PSequence([(notesInChord[0]+element,notesInChord[1]+element,notesInChord[2]+element) for element in chord_sequence])

timeline = Timeline(60)
timeline.clear()
timeline = Timeline(durationChords*len(chord_sequence)/8)

timeline.schedule({
    "degree": iso.PSequence([9, 7, 3, 0]),
    "key": key_sequence,
    "octave": 5,
    "duration": durationChords/8,
    "amplitude": 25,
})

instrument = Dreamstrument(
    path = "sounds/instruments/voices/essentialWorkers-pad1"
)

midi = timeline.to_midi()
comp = instrument.render_midi(midi)
comp.fade_out(500).export("output/synthTest2.mp3")