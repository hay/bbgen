from math import log10

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