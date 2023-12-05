from scipy.io import wavfile
from mido import MidiTrack, MidiFile
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import dawdreamer as daw
import librosa

BUFFER_SIZE:int = 512
MIDDLE_C:int = 60
SAMPLE_RATE:int = 44100

class Dreampler:
    def __init__(self, segment:AudioSegment, root_note:int = MIDDLE_C):
        self.root_note = root_note

        # Dawdreamer is quite a beast to initialize
        inp_file = NamedTemporaryFile(suffix = ".wav")
        segment.export(inp_file, format = "wav")
        self.engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
        sig, sr = librosa.load(inp_file.name, sr = SAMPLE_RATE, mono = False)
        self.sampler = self.engine.make_sampler_processor("playback", sig)
        self.param_desc = self.sampler.get_parameters_description()
        self.sampler.set_parameter(self.param_index("Center Note"), self.root_note)

    def param_index(self, name:str) -> int:
        for param in self.param_desc:
            if param["name"] == name:
                return param["index"]

        raise ValueError(f"Parameter '{name}' not found.")

    def render_midi(self, midi:MidiFile) -> AudioSegment:
        # Create a new segment that is the length of the complete composition
        print(f"Rendering midi file of {midi.length} length")

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