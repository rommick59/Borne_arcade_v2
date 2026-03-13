from dataclasses import dataclass
from core.enums import Ingredient, CakeType

@dataclass(frozen=True)
class Recipe:
    cake_type:   CakeType
    ingredients: tuple  # tuple[Ingredient, ...]
    reward:      int
    time_limit:  float
    weight:      int = 10  # relative spawn probability (higher = more common)
