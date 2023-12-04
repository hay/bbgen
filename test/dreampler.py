import sys
sys.path.append("..")

from bbgen.dreampler import Dreampler
from bbgen.midi import Midi
from pydub import AudioSegment

mozart = Midi("mozart.mid")
clarinet = AudioSegment.from_wav("clarinet.wav")
dreampler = Dreampler(clarinet)

# Render complete midi file using the same crapler
dreampler.render_midi(mozart).export("output/mozart-clarinet.mp3")

# Render a single track
dreampler.render_track(mozart.get_track(1)).export("output/mozart-clarinet-track.mp3")