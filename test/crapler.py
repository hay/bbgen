import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi
from pydub import AudioSegment

mozart = Midi("mozart.mid")
meow = AudioSegment.from_wav("meow.wav")[0:200]
crapler = Crapler(meow)

# First render the first track, then just loop over the rest
comp = None
for track in mozart.tracks:
    rendered = crapler.render(track)

    if comp:
        comp = comp.overlay(rendered)
    else:
        comp = rendered

comp.export("meowzart.mp3")