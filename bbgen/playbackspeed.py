from bbgen.timestretch import TimeStretch
from dataclasses import dataclass
from loguru import logger
from math import log
from pydub import AudioSegment

@dataclass
class Playbackspeed:
    rate: float = 1
    high_quality: bool = True

    def apply(self, segment:AudioSegment) -> AudioSegment:
        logger.info(f"Applying Playbackspeed {self.rate}")

        # Convert rate to semitones
        pitch = log(self.rate ** 12) / log(2)

        ts = TimeStretch(
            stretch = self.rate,
            pitch = pitch,
            high_quality = self.high_quality
        )

        return ts.apply(segment)