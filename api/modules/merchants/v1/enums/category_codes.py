from enum import Enum


class CategoryCodes(Enum):
    food: tuple[str] = "5411", "5412"
    meal: tuple[str] = "5811", "5812"

    @classmethod
    def list(cls) -> tuple[str]:
        return cls.food.value + cls.meal.value
