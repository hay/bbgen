import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi
from pydub import AudioSegment

midi = Midi("satie.mid")
instrument = AudioSegment.from_wav("clarinet.wav")
crapler = Crapler(instrument)

# Render complete midi file using the same crapler
crapler.render_midi(midi).export("output/satie-crapler.mp3")

# Render a single track
crapler.render_track(midi.get_track(1)).export("output/satie-crapler-track.mp3")