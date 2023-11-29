from bbgen.midi import Midi
from bbgen.paulstretch import Paulstretch
from bbgen.soundfont import Soundfont
from bbgen.wave import Wave

sf = Soundfont("./FluidR3Mono_GM.sf3")

score1 = "4/4 C4 trip{C8 D E} trip{F4 G A} B-1"

wave = Midi.from_tinynotation(score1).render(sf).effect(Paulstretch())
wave2 = Wave(wave.as_tmpfile()).reverse()
wave.overlay(wave2, position = 100).write("layers.mp3", format = "mp3")