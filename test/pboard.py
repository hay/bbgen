import sys
sys.path.append("..")

from bbgen.effects import PedalboardProcessor, Playbackspeed, TimeStretch
from pedalboard import Pedalboard, Chorus, Reverb, Phaser
from pydub import AudioSegment

board = Pedalboard([Phaser(), Chorus(), Reverb(room_size=1)])
chico = AudioSegment.from_mp3("chico.mp3")[1000:2000] + AudioSegment.silent(duration = 3000)
chico = PedalboardProcessor(board).apply(chico)
chico = Playbackspeed(.25).apply(chico)
chico = TimeStretch(pitch = 12).apply(chico)
chico.export("chico-pboard.mp3")