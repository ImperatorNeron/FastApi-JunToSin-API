import enum


class Complexity(enum.Enum):
    VERY_EASY = "Effortless"
    EASY = "Easy"
    MODERATE = "Moderate"
    CHALLENGING = "Challenging"
    DIFFICULT = "Difficult"
    VERY_DIFFICULT = "Complicated"


class Status(enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
