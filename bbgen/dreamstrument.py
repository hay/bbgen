from bbgen.dreampler import Dreampler, SAMPLE_RATE
from bbgen.soundbank import Soundbank
from bbgen.util import get_notes_from_midi
from loguru import logger
from mido import MidiFile
from pathlib import Path
from pydub import AudioSegment
from scipy.io import wavfile
from tempfile import NamedTemporaryFile
import re

RE_NOTE_PATTERN = re.compile(r'^(\d+)\.')

class Dreamstrument:
    def __init__(self, path:str, suffix = "wav", pattern = RE_NOTE_PATTERN, round_robin:bool = False):
        logger.debug("Initializing Dreamstrument")
        self.path = Path(path)
        self.suffix = suffix
        self.pattern = pattern
        self.soundbank = Soundbank(round_robin = round_robin)
        self.load_soundbank()

    def load_soundbank(self):
        # Iterate over all the samples in a directory and create samples
        # based on the file
        for path in self.path.glob(f"*.{self.suffix}"):
            logger.debug(f"Trying to create Dreampler from sample {path}")
            match = self.pattern.findall(str(path.stem));

            if len(match) == 0:
                raise Exception(f"Could not load soundbank {self.path}")

            note = int(match[0])
            segment = AudioSegment.from_wav(path)
            sampler = Dreampler(segment, note)
            self.soundbank.add_sampler(note, sampler)

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        length = midi.length
        logger.debug(f"Rendering midi file of {length} length, PPQN is {midi.ticks_per_beat}")
        comp = AudioSegment.silent(duration = length * 1000)

        for n in get_notes_from_midi(midi):
            logger.debug(f"Render note: {n}")
            note = n["note"]
            time = n["time"]

            # Need to add these two values somewhere
            duration = n["duration"]
            velocity = n["velocity"]

            # FIXME this is obviously a terrible hack
            # We need to figure out how the graph works and reset that instead
            # of just re-creating the Dreampler
            s = self.soundbank.get_sampler_by_note(note)
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

        return comp