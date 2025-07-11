"""
Robocar Project - Система управления роботом голосом и жестами
"""

from .robot import Robot
from modules.hand_detector import HandDetector
from modules.camera import TapoCamera
from modules.movement import MovementController
from modules.lighting import LightController
from modules.voice_control import VoiceController
from modules.gesture_control import GestureController

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
