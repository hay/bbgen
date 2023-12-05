import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi, get_notes_from_track
from mido import MidiFile
from pydub import AudioSegment
import json
import mido

midi = MidiFile("satie.mid")
print(midi, midi.length)

# crapler = Crapler(AudioSegment.from_wav("./clarinet.wav"))
# midi = Midi("satie.mid")
# crapler.render_track(midi.tracks[0]).export("output/crapler-notes.mp3")

# print(json.dumps(get_notes_from_track(midi.tracks[1]), indent = 4))