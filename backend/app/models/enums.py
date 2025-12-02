"""
Enums shared between models and schemas
"""
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MizajType(str, Enum):
    GARM = "garm"
    SARD = "sard"
    TAR = "tar"
    KHOSHK = "khoshk"
    GARM_TAR = "garm_tar"
    GARM_KHOSHK = "garm_khoshk"
    SARD_TAR = "sard_tar"
    SARD_KHOSHK = "sard_khoshk"
    MOTADEL = "motadel"

