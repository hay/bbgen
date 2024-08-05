from loguru import logger
from random import choice

class Soundbank:
    def __init__(self, round_robin:bool = True):
        self.samplers = {}
        self.round_robin = round_robin
        logger.info(f"Initializing soundbank, round robin: {round_robin}")

    def add_sampler(self, note:int, sampler):
        if note in self.samplers:
            self.samplers[note]["samplers"].append(sampler)
        else:
            self.samplers[note] = {
                "index" : 0,
                "samplers" : [ sampler ]
            }

    def get_sampler_by_note(self, note:int):
        closest_note = min(self.samplers.keys(), key=lambda x: abs(x - note))
        sampler = self.samplers[closest_note]

        # Get the next sampler, if we're using round_robin,
        # otherwise use choice to get a random sampler
        if self.round_robin:
            next_index = (sampler["index"] + 1) % len(sampler["samplers"])
            logger.debug(f"Round robin note: {note}/{next_index}")
            smp = sampler["samplers"][next_index]
            sampler["index"] = next_index
            return smp
        else:
            return choice(sampler["samplers"])