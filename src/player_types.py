# types.py

# This file defines any necessary types or constants used throughout the application.

from typing import Tuple

# Define a type for video player options
VideoPlayerOptions = Tuple[int, int]  # width, height

# Define constants for control events
class ControlEvents:
    PLAY = "play"
    PAUSE = "pause"
    STOP = "stop"