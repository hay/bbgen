import sys
sys.path.append("..")

from bbgen.dreampler import Dreampler, SAMPLE_RATE
from bbgen.fluidsynth import FluidSynth
from bbgen.isobar import Timeline
from bbgen.util import get_notes_from_midi
from mido import MidiFile
from pathlib import Path
from pydub import AudioSegment
from scipy.io import wavfile
from tempfile import NamedTemporaryFile
import isobar as iso

# seq = iso.PSequence([0, 2, 7, 3]) + 36
# seq = iso.PStutter(seq, 3) + iso.PSequence([0, 12, 24])

# timeline = Timeline(12)

# timeline.schedule({
#     "note": seq,
#     "duration": 1,
# })

# midi = timeline.to_midi()
midi = MidiFile("satie.mid")
# FluidSynth("./FluidR3Mono_GM.sf3").render_midi(midi).export("output/instrument-fluidsynth.mp3")
# exit()

from random import choice
import re
RE_PATTERN = re.compile(r'^(\d+)\.')

class Soundbank:
    def __init__(self, round_robin:bool = True):
        self.samplers = {}
        self.round_robin = round_robin

    def add_sampler(self, note:int, sampler):
        if note in self.samplers:
            self.samplers[note]["samplers"].append(sampler)
        else:
            self.samplers[note] = {
                "index" : 0,
                "samplers" : [ sampler ]
            }

    def get_sampler_by_note(self, note:int):
        closest_note = min(self.samplers.keys(), key=lambda x: abs(x - note))
        sampler = self.samplers[closest_note]

        # Get the next sampler, if we're using round_robin,
        # otherwise use choice to get a random sampler
        if self.round_robin:
            next_index = (sampler["index"] + 1) % len(sampler["samplers"])
            return sampler["samplers"][next_index]
        else:
            return choice(sampler["samplers"])

# First iterate over all the samples in a directory and create samples
# based on the file
sb = Soundbank()

for path in Path("12string_piano").glob("*.wav"):
    match = RE_PATTERN.findall(str(path.stem));
    note = int(match[0])
    segment = AudioSegment.from_wav(path)
    sampler = Dreampler(segment, note)
    sb.add_sampler(note, sampler)

# Create a new segment that is the length of the complete composition
length = midi.length
print(f"Rendering midi file of {length} length, PPQN is {midi.ticks_per_beat}")
comp = AudioSegment.silent(duration = length * 1000)
sampler = Dreampler(AudioSegment.from_wav("clarinet.wav"))

for n in get_notes_from_midi(midi):
    print(n)
    note = n["note"]
    time = n["time"]

    # Need to add these two values somewhere
    duration = n["duration"]
    velocity = n["velocity"]

    # FIXME this is obviously a terrible hack
    # We need to figure out how the graph works and reset that instead
    # of just re-creating the Dreampler
    s = sb.get_sampler_by_note(note)
    sampler = Dreampler(s.segment, s.root_note)

    sampler.sampler.add_midi_note(note, velocity, 0, duration)
    sampler.engine.load_graph([
        (sampler.sampler, [])
    ])
    sampler.engine.render(duration * 2) # Render for the double amount of time because for some reason release is not calculated
    output = sampler.engine.get_audio()
    outfile = NamedTemporaryFile(suffix = ".wav")
    wavfile.write(outfile.name, SAMPLE_RATE, output.transpose())
    segment = AudioSegment.from_wav(outfile.name)
    outfile.close()

    comp = comp.overlay(segment, position = time * 1000)

comp.export("output/instrument-dreampler.mp3")