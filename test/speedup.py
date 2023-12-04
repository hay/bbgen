import sys
sys.path.append("..")

from bbgen.effects import Playbackspeed
from pydub import AudioSegment
import wave

hammond = AudioSegment.from_wav("clarinet.wav")
Playbackspeed(0.5).apply(hammond).export("output/clarinet-slow.mp3")