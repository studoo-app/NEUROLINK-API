from enum import Enum

class Category(str, Enum):
    NEURAL = "Neural"
    SENSORY = "Sensory"
    MOTOR = "Motor"
    METABOLIC = "Metabolic"
    CARDIOVASCULAR = "Cardiovascular"
    DERMAL = "Dermal"


class Severity(str, Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"


class ApiKeyRole(str, Enum):
    USER = "User"
    ADMIN = "Admin"
    SUPERADMIN = "SuperAdmin"
