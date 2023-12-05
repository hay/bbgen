import sys
sys.path.append("..")

from bbgen.fluidsynth import FluidSynth
from mido import MidiFile

midi = MidiFile("satie.mid")
synth = FluidSynth("./FluidR3Mono_GM.sf3")
synth.render_midi(midi).export("output/satie-fluidsynth.mp3")