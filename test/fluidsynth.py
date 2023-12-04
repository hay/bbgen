import sys
sys.path.append("..")

from bbgen.soundfont import Soundfont
from bbgen.midi import Midi
from bbgen.effects import Paulstretch

arp1 = Midi("satie.mid").set_program(0, 90)
audio = arp1.render(soundfont = Soundfont("./FluidR3Mono_GM.sf3"))
audio.export("output/satie.mp3", format = "mp3")