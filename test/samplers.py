import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.dreampler import Dreampler
from bbgen.fluidsynth import FluidSynth
from mido import MidiFile
from pydub import AudioSegment

midi = MidiFile("satie.mid")
synth = FluidSynth("./FluidR3Mono_GM.sf3")
clarinet = AudioSegment.from_wav("clarinet.wav")

Crapler(clarinet).render_midi(midi).export("output/satie-crapler.mp3")
# Dreampler(clarinet).render_midi(midi).export("output/satie-dreampler.mp3")

# synth.render_midi(midi).export("output/satie-fluidsynth.mp3")