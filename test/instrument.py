import sys
sys.path.append("..")

from bbgen.dreamstrument import Dreamstrument
from loguru import logger
from mido import MidiFile

# logger.enable("bbgen")

midi = MidiFile("satie.mid")
instrument = Dreamstrument(
    path = "raindrop_c40",
    round_robin = True
)
instrument.render_midi(midi).export("output/instrument-dreampler.mp3")