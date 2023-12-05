import sys
sys.path.append("..")


from bbgen.isobar import Timeline
from bbgen.midi import Midi
from pydub import AudioSegment
import isobar as iso
from bbgen.dreampler import Dreampler

key_sequence = iso.PSequence([
    iso.Key("C", "minor"),
    iso.Key("G", "minor"),
    iso.Key("Bb", "major"),
    iso.Key("F", "major"),
])
key = iso.PStaticPattern(key_sequence, 4)
timeline = Timeline(120)
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

timeline.run()
timeline.output.write()
midi = Midi(timeline.file.name)

instrument = AudioSegment.from_wav("clarinet.wav")
dreampler = Dreampler(instrument)



dreampler.render_midi(midi).export("chords.mp3")
