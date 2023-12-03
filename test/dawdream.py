Render a single track
crapler.render_track(mozart.get_track(1)).export("mozart-track.mp3")

from scipy.io import wavfile
import dawdreamer as daw
import librosa

BUFFER_SIZE = 512
SAMPLE_RATE = 44100

def get_param_index(desc, name):
    for d in desc:
        if d["name"] == name:
            return d["index"]

# Samples need to be either mono or stero 44.1khz 16-bit WAV files
# everything else will fail!

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
sig, sr = librosa.load("clarinet.wav", sr = SAMPLE_RATE, mono = False)
sampler = engine.make_sampler_processor("playback", sig)
desc = sampler.get_parameters_description()
center_note_index = get_param_index(desc, "Center Note")
sampler.set_parameter(center_note_index, 60)
sampler.load_midi("mozart.mid")
engine.load_graph([
    (sampler, [])
])
engine.render(15)
output  = engine.get_audio()
wavfile.write("mozart-piano.wav", SAMPLE_RATE, output.transpose())