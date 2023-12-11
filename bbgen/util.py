from math import log10
from mido import MidiFile, MidiTrack, Message

def get_notes_from_midi(midi:MidiFile) -> list:
    time = 0
    notes = []

    for msg in midi:
        time = time + msg.time

        if msg.type == "note_on":
            notes.append({
                "note" : msg.note,
                "velocity" : msg.velocity,
                "time" : time
            })

        if msg.type == "note_off":
            for note in notes:
                if note["note"] == msg.note:
                    note["duration"] = time - note["time"]

    # Make sure note always have a duration
    for note in notes:
        if "duration" not in note:
            # TODO: should this be one?
            note["duration"] = 1

    return notes

# Loop over a track and change all instances of program_change to the program
# If that's not in the file, add it
def set_midi_program_for_track(track:MidiTrack, program:int) -> MidiTrack:
    has_track = False

    for msg in track:
        if msg.type == "program_change":
            msg.program = program
            has_track = True

    if not has_track:
        track.insert(0, Message("program_change", program = program))


def velocity_to_db(velocity, a = 6, b = -60):
    return a * log10(velocity + 1) + b