import sys
sys.path.append("..")

from bbgen.effects import PedalboardProcessor, Playbackspeed, TimeStretch
from pedalboard import Pedalboard, Chorus, Reverb, Phaser
from pydub import AudioSegment
from random import randint, random

board = Pedalboard([Phaser(), Chorus(), Reverb(room_size=1)])
start = randint(0, 2000)
music = AudioSegment.from_mp3("music.mp3")[start:start + 1000] + AudioSegment.silent(duration = 10000)
music = PedalboardProcessor(board).apply(music)
music = Playbackspeed(random()).apply(music)
music = TimeStretch(pitch = randint(-12, 12)).apply(music)
start = randint(0, 2000)
comp = music.overlay(TimeStretch(pitch = randint(-12, 12)).apply(music), position = start)
comp = comp.overlay(TimeStretch(pitch = randint(-12, 12)).apply(music), position = start + 3000)

comp.export("output/music-pboard.mp3")