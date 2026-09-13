from enum import Enum


class Tier(str, Enum):
    SALVAGE = "Salvage"
    STANDARD = "Standard"
    CLINICAL = "Clinical"
    PRIME = "Prime"
    MILSPEC = "MilSpec"
    PROTOTYPE = "Prototype"

class Category(str,Enum):
    NEURAL = "Neural"
    SENSORY = "Sensory"
    MOTOR = "Motor"
    METABOLIC = "Metabolic"
    CARDIOVASCULAR = "Cardiovascular"
    DERMAL = "Dermal"