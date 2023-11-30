import sys
sys.path.append("..")

from bbgen.effects import PitchShift
from pydub import AudioSegment

hammond = AudioSegment.from_wav("hammond.wav")
comp = None

for octave in (-2, 0, 2):
    melody = AudioSegment.silent()

    for tone in (0, 2, 6, 2, 6, 1, 3):
        effect = PitchShift(semitones = tone + octave)
        melody = melody + effect.apply(hammond)

    if not comp:
        comp = AudioSegment.silent(duration = len(melody))

    comp = comp.overlay(melody)

comp.export("hammond.mp3", format = "mp3")