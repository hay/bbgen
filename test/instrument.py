import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from mido import MidiFile

midi = MidiFile("satie.mid")
instrument = Dreamstrument(
    path = "raindrop_c40"
)
instrument.render_midi(midi).export("output/instrument-dreampler.mp3")