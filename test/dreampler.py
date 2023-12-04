import sys
sys.path.append("..")

from bbgen.dreampler import Dreampler
from bbgen.midi import Midi
from pydub import AudioSegment

midi = Midi("satie.mid")
instrument = AudioSegment.from_wav("clarinet.wav")
dreampler = Dreampler(instrument)

# Render complete midi file using the same crapler
dreampler.render_midi(midi).export("output/satie-dreampler.mp3")

# Render a single track
dreampler.render_track(midi.get_track(1)).export("output/satie-dreampler-track.mp3")