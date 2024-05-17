import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from bbgen.effects import PedalboardProcessor
from bbgen.isobar import Timeline
from pedalboard import Pedalboard, Reverb, Delay, Convolution
from pydub import AudioSegment
import random
import isobar as iso

# Choice with a seed
def choice_with_seed(lst:list, seed:int):
    random.seed(seed)
    return random.choice(lst)

def generate_sequence(length:int, seed:int) -> list:
    notes = [0, 2, 4, 5, 7, 9, 11]
    melody = [ choice_with_seed(notes, seed) ]

    for i in range(1, length):
        # Get the last note added to the melody
        last_note = melody[-1]

        # Find the index of the last note in the scale
        last_note_index = notes.index(last_note)

        # Choose the next note index with a preference for stepwise motion
        next_note_index_options = [max(last_note_index - 1, 0), last_note_index, min(last_note_index + 1, len(notes) - 1)]
        next_note_index = choice_with_seed(next_note_index_options, seed)

        # Add the next note to the melody
        melody.append(notes[next_note_index])

    return melody

# simpele sequentie
# chord_sequence = [9, 6, 12, 8] # @param {type:"raw"}
# noten om te spelen
# notesInChord = [0, 2, 5] # @param {type:"raw"}
SEED = 100
chord_sequence = generate_sequence(4, SEED)
notesInChord = generate_sequence(3, SEED)
print("chord_sequence", chord_sequence)
print("notesInChord", notesInChord)


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
    "amplitude": 80,
})

instrument = Dreamstrument(
    path = "samples/12string_piano"
)

midi = timeline.to_midi()
comp = instrument.render_midi(midi)

# Add some silence to make sure the echo/delay causes a nice fadeout
comp = comp + AudioSegment.silent(10000)

# Add delay effects
board = Pedalboard([
    Delay(0.5, feedback = 0.5, mix = 0.3),
    Reverb(room_size=0.7, wet_level = 0.5, dry_level = 0.5),
    Convolution("samples/reverb/underwater2.wav")
])
comp = PedalboardProcessor(board).apply(comp)

# And export
comp.export("output/intersynth.mp3")