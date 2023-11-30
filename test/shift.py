import sys
sys.path.append("..")

from bbgen.pitchshift import PitchShift
from bbgen.wave import Wave

hammond = Wave("hammond.wav")
melody = Wave() # Empty to append other stuff to

for tone in range(12):
    effect = PitchShift(semitones = tone)
    melody.append(hammond.effect(effect))

melody.write("hammond.mp3", format = "mp3")