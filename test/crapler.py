import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi
from pydub import AudioSegment

mozart = Midi("mozart.mid")
meow = AudioSegment.from_wav("meow.wav")[0:200]
crapler = Crapler(meow)

# Render complete midi file using the same crapler
crapler.render_midi(mozart).export("meowzart-complete.mp3")

# Render a single track
crapler.render_track(mozart.get_track(1)).export("meowzart-track.mp3")