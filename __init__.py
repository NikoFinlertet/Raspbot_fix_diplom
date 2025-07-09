"""
Robocar Project - Система управления роботом голосом и жестами
"""

from .robot import Robot
from .hand_detector import HandDetector
from .camera import TapoCamera
from .movement import MovementController
from .lighting import LightController
from .voice_control import VoiceController
from .gesture_control import GestureController

__version__ = "1.0.0"
__author__ = "Hohma Team"

__all__ = [
    "Robot",
    "HandDetector",
    "TapoCamera",
    "MovementController",
    "LightController",
    "VoiceController",
    "GestureController"
]
