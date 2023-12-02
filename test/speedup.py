import sys
sys.path.append("..")

from bbgen.effects import Playbackspeed
from pydub import AudioSegment
import wave

hammond = AudioSegment.from_wav("hammond.wav")
Playbackspeed(0.5).apply(hammond).export("hammond-slow.mp3")