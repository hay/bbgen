import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.midi import Midi
from pydub import AudioSegment

mozart = Midi("mozart.mid")
meow = AudioSegment.from_wav("meow.wav")[0:200]
crapler = Crapler(meow)

track1 = crapler.render(mozart.get_track(1))
track2 = crapler.render(mozart.get_track(2))
track2.overlay(track1).export("meowzart.mp3")