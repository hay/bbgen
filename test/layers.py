import sys
sys.path.append("..")

from bbgen.effects import Paulstretch
from bbgen.midi import Midi
from bbgen.soundfont import Soundfont

sf = Soundfont("./FluidR3Mono_GM.sf3")

score1 = "4/4 C4 trip{C8 D E} trip{F4 G A} B-1"

wave = Midi.from_tinynotation(score1).render(sf)
wave = Paulstretch().apply(wave)
wave.overlay(wave.reverse(), position = 100).export("layers.mp3")