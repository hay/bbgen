# A wrapper around the regular isobar timeline
# to faciliate exporting / rendering
from isobar.io import MidiFileOutputDevice
from isobar import Timeline as IsoTimeline
from mido import MidiFile
from tempfile import NamedTemporaryFile
import isobar as iso

class Timeline(IsoTimeline):
    def __init__(self, beats):
        self.file = NamedTemporaryFile()
        self.output = MidiFileOutputDevice(self.file.name)
        super().__init__(iso.MAX_CLOCK_RATE, output_device = self.output)
        self.stop_when_done = True

        # Note that we need beats to make sure the thing actually stops
        # See < https://github.com/ideoforms/isobar/issues/49 >
        self.schedule({
            "action" : lambda: self.clear()
        }, delay = beats)

    def to_midi(self) -> MidiFile:
        self.run()
        self.output.write()
        return MidiFile(self.file.name)