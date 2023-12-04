import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi
from pydub import AudioSegment

mozart = Midi("mozart.mid")
meow = AudioSegment.from_wav("clarinet.wav")[0:500]
crapler = Crapler(meow)

# Render complete midi file using the same crapler
crapler.render_midi(mozart).export("output/mozart-complete.mp3")

# Render a single track
crapler.render_track(mozart.get_track(1)).export("output/mozart-track.mp3")