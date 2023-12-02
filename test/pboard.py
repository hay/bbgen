import sys
sys.path.append("..")

from bbgen.effects import PedalboardProcessor, Playbackspeed
from pedalboard import Pedalboard, Chorus, Reverb, Phaser
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

board = Pedalboard([Phaser(), Chorus(), Reverb(room_size=1)])
chico = AudioSegment.from_mp3("chico.mp3")[0:1000] + AudioSegment.silent(duration = 3000)
chico = PedalboardProcessor(board).apply(chico)
chico = Playbackspeed(0.5).apply(chico)
chico.export("chico-pboard.mp3")