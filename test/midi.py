import sys
sys.path.append("..")

from bbgen.midi import Midi, get_notes_from_track
import json
midi = Midi("satie.mid")
print(json.dumps(get_notes_from_track(midi.tracks[1]), indent = 4))