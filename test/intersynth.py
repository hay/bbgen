import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from bbgen.effects import PedalboardProcessor
from bbgen.isobar import Timeline
from pedalboard import Pedalboard, Reverb, Delay
from pydub import AudioSegment
import isobar as iso

# simpele sequentie
chord_sequence = [9, 6, 12, 8] # @param {type:"raw"}

# noten om te spelen
notesInChord = [0, 2, 5] # @param {type:"raw"}

# toonladder
note_name = 'C' # @param ['C', 'D', 'E', 'F', 'G', 'A', 'B']
key_types = 'major' # @param ['major', 'minor', 'pureminor', 'puremajor', 'augmented', 'fourths']
key_sequence = iso.Key(note_name, key_types) # type: ignore

# Construct the sequence where we take the notes to play in the chord,
# and use the chord_sequence
sequence_notes = []
for chord in chord_sequence:
    sequence_notes.append((
        notesInChord[0] + chord,
        notesInChord[1] + chord,
        notesInChord[2] + chord
    ))

chord_sequence = iso.PSequence(sequence_notes)

durationChords = 8

key = iso.PStaticPattern(key_sequence, 4)
timeline = Timeline(30)
timeline.schedule({
    "degree": chord_sequence,
    "key": key,
    "octave": 3,
    "duration": durationChords,
    "amplitude": 40,
})

instrument = Dreamstrument(
    path = "samples/12string_piano"
)

midi = timeline.to_midi()
comp = instrument.render_midi(midi)

# Add some silence to make sure the echo/delay causes a nice fadeout
comp = comp + AudioSegment.silent(5000)

# Add delay effects
board = Pedalboard([
    Delay(0.5, feedback = 0.5, mix = 0.3),
    Reverb(room_size=0.7, wet_level = 0.5, dry_level = 0.5)
])
comp = PedalboardProcessor(board).apply(comp)

# And export
comp.export("output/intersynth.mp3")