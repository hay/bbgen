import sys
sys.path.append("..")

from bbgen.isobar import Timeline
from bbgen.soundfont import Soundfont
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
        iso.Key("A", "minor"),
        iso.Key("F"),
        iso.Key("C"),
        iso.Key("G"),
    ])

    key = iso.PStaticPattern(key_sequence, 4)

    timeline.schedule({
        "degree": 0,
        "key": key,
        "octave": 3
    })

    timeline.schedule({
        "degree": iso.PCreep(iso.PWhite(0, 6), 2, 2, 3),
        "key": key,
        "octave": 4,
        "duration": 0.25
    })

timeline = Timeline(beats = 64)
chords(timeline)
timeline.render(Soundfont("./FluidR3Mono_GM.sf3")).export("output/ibar.mp3", format = "mp3")
>>>>>>> Stashed changes
