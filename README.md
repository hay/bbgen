# bbgen
> A Python library for generative music

By [Hay Kranen](http://www.haykranen.nl)

## Introduction
bbgen is a Python library that allows you to make generative music. It is designed for non-realtime use: you shouldn't be using this library for a performance.

bbgen is a wrapper around a couple of other libraries that perform most of the heavy lifting, this includes [pydub](https://pydub.com/) for composing / editing audio files, [pedalboard](https://spotify.github.io/pedalboard/index.html) for effects, [dawdreamer](https://github.com/DBraun/DawDreamer) for rendering midi and [isobar](https://ideoforms.github.io/isobar/) for generating the music.

bbgen is most definitely a work in progress, and it desperately needs documentation which i haven't written yet. But you can look in the `test` folder for a couple of examples.

I have ran bbgen on macOS 14.6.1 on an Apple M1 processor, and it also works on Linux (Ubuntu 22.04 LTS). I haven't tested on Windows yet.

Render a MIDI file using a sampler like this:
```python
from bbgen.dreampler import Dreampler
from mido import MidiFile, Message
from pydub import AudioSegment

midi = MidiFile("satie.mid")
clarinet = AudioSegment.from_wav("clarinet.wav")

Dreampler(clarinet).render_midi(midi).export("satie-dreampler.mp3")
```

## Install
You probably need to install [Fluidsynth](https://www.fluidsynth.org/) and i guess ffmpeg as well.

I've tested bbgen on Python 3.10. It might run on newer versions as well but i haven't tested that yet.

This is should work:
1. Clone this repo
```bash
git clone https://github.com/hay/bbgen.git
```

2. Make a virtual environment and install the `requirements.txt`
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Try running the `samplers.py` example in `test` to showcase the three different samples available in bbgen:
```bash
cd test
python samplers.py
```

## Things to do:
🔲 Documentation
🔲 Speed up the samplers (esp. `Dreampler` and `Dreamstrument` are very slow)

## License
MIT &copy; [Hay Kranen](http://www.haykranen.nl)