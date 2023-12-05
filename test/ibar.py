import sys
sys.path.append("..")

from bbgen.fluidsynth import FluidSynth
from bbgen.isobar import Timeline
import isobar as iso

def reich(timeline):
    sequence = iso.PSequence([-7, -5, 0, 2, 3, -5, -7, 2, 0, -5, 3, 2])
    timeline.schedule({
        "note": sequence.copy() + 60,
        "duration": 0.5
    })

    timeline.schedule({
        "note": sequence.copy() + 72,
        "duration": 0.5 * 1.01
    })

def stochastic(timeline):
    notes = iso.PLSystem("N[+N--?N]+N[+?N]", depth=4)
    notes = iso.PDegree(notes, iso.Scale.majorPenta)
    notes = notes % 36 + 52

    timeline.schedule({
        "note": notes,
        "duration": 0.25
    })

def chords(timeline):
    key_sequence = iso.PSequence([
        iso.Key("C", "minor"),
        iso.Key("G", "minor"),
        iso.Key("Bb", "major"),
        iso.Key("F", "major"),
    ])
    key = iso.PStaticPattern(key_sequence, 4)
    timeline.schedule({
        "degree": 0,
        "key": key,
        "octave": 3,
        "duration": 3,
    })

    timeline.schedule({
        "degree": 3,
        "key": key,
        "octave": 4,
        "duration": 3
    })

    timeline.schedule({
        "degree": 5,
        "key": key,
        "octave": 4,
        "duration": 3
    })

timeline = Timeline(60)
chords(timeline)
FluidSynth("./FluidR3Mono_GM.sf3").render_midi(timeline.to_midi()).export("output/ibar.mp3")