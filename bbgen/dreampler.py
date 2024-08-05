from loguru import logger
from mido import MidiTrack, MidiFile
from pydub import AudioSegment
from scipy.io import wavfile
from tempfile import NamedTemporaryFile
import dawdreamer as daw
import librosa

BUFFER_SIZE:int = 512
MIDDLE_C:int = 60
SAMPLE_RATE:int = 44100

# NOTE that files for the Dreampler should be in 44.1khz stereo 16bit
class Dreampler:
    def __init__(self, segment:AudioSegment, root_note:int = MIDDLE_C):
        if not isinstance(segment, AudioSegment):
            raise Exception(f"Segment is not an AudioSegment but {type(segment)}: {segment}")

        logger.info(f"Initializing Dreampler with segment {segment}, root_note is {root_note}")
        self.root_note = root_note
        self.segment = segment

        # Dawdreamer is quite a beast to initialize
        inp_file = NamedTemporaryFile(suffix = ".wav")
        segment.export(inp_file, format = "wav")
        self.engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
        sig, sr = librosa.load(inp_file.name, sr = SAMPLE_RATE, mono = False)

        try:
            self.sampler = self.engine.make_sampler_processor("playback", sig)
        except IndexError as e:
            logger.error("Got an error. Are you sure your files are stereo?")
            raise(e)

        self.param_desc = self.sampler.get_parameters_description()
        self.set_param("Center Note", self.root_note)
        self.set_adsr()

    def param_index(self, name:str) -> int:
        for param in self.param_desc:
            if param["name"] == name:
                return param["index"]

        raise ValueError(f"Parameter '{name}' not found.")

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        logger.info(f"Rendering midi file of {midi.length} length")

        infile = NamedTemporaryFile(suffix = ".mid")
        midi.save(infile.name)

        self.sampler.load_midi(infile.name)
        self.engine.load_graph([
            (self.sampler, [])
        ])
        self.engine.render(midi.length)
        output = self.engine.get_audio()

        outfile = NamedTemporaryFile(suffix = ".wav")
        wavfile.write(outfile.name, SAMPLE_RATE, output.transpose())
        segment = AudioSegment.from_wav(outfile.name)

        infile.close()
        outfile.close()

        return segment

    def set_adsr(self, attack = 0, decay = 0, sustain = 1, release = 100):
        self.set_param("Amp Env Attack", attack)
        self.set_param("Amp Env Decay", decay)
        self.set_param("Amp Env Sustain", sustain)
        self.set_param("Amp Env Release", release)

    def set_param(self, name:str, value):
        self.sampler.set_parameter(self.param_index(name), value)