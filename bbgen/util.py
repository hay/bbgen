from math import log10
from mido import MidiTrack

def velocity_to_db(velocity, a = 6, b = -60):
    """
    Convert MIDI velocity to decibels using a logarithmic scale.
    
    Parameters:
    - velocity: MIDI velocity value (0 to 127)
    - a: Constant for scaling the logarithmic value (adjust as needed)
    - b: Constant for offset (adjust as needed)
    
    Returns:
    - db: Decibels
    """
    return a * log10(velocity + 1) + b

def get_notes_from_track(track:MidiTrack) -> list:
    print(track)
    notes = []
    time = 0

    for msg in track:
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

    return {
        "total_time" : time,
        "notes" : notes
    }