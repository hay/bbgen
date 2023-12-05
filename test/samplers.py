import sys
sys.path.append("..")

from bbgen.crapler import Crapler
from bbgen.dreampler import Dreampler
from bbgen.fluidsynth import FluidSynth
from bbgen.util import set_midi_program_for_track
from mido import MidiFile, Message
from pydub import AudioSegment

midi = MidiFile("satie.mid")
synth = FluidSynth("./FluidR3Mono_GM.sf3")
clarinet = AudioSegment.from_wav("clarinet.wav")

Crapler(clarinet).render_midi(midi).export("output/satie-crapler.mp3")
Dreampler(clarinet).render_midi(midi).export("output/satie-dreampler.mp3")

# Set clarinet as instrument for general midi
for track in midi.tracks:
    set_midi_program_for_track(track, 71)

synth.render_midi(midi).export("output/satie-fluidsynth.mp3")