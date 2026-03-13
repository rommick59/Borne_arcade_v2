import random
from core.enums import Ingredient, CakeType
from recipe.recipe import Recipe

class RecipeCatalog:
    """Source unique de toutes les recettes du jeu."""

    _recipes: dict = {
        # --- Recettes classiques (communes) ---
        CakeType.VANILLA_CAKE: Recipe(
            cake_type   = CakeType.VANILLA_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.VANILLA),
            reward      = 100,
            time_limit  = 60.0,
            weight      = 12,
        ),
        CakeType.CHOCOLATE_CAKE: Recipe(
            cake_type   = CakeType.CHOCOLATE_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.CHOCOLATE),
            reward      = 120,
            time_limit  = 55.0,
            weight      = 12,
        ),
        CakeType.STRAWBERRY_CAKE: Recipe(
            cake_type   = CakeType.STRAWBERRY_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.STRAWBERRY, Ingredient.CREAM),
            reward      = 150,
            time_limit  = 50.0,
            weight      = 10,
        ),
        CakeType.CREAM_PUFF: Recipe(
            cake_type   = CakeType.CREAM_PUFF,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.CREAM),
            reward      = 80,
            time_limit  = 45.0,
            weight      = 12,
        ),
        # --- Recettes absurdes (peu communes) ---
        CakeType.CHEWING_GUM_CAKE: Recipe(
            cake_type   = CakeType.CHEWING_GUM_CAKE,
            ingredients = (Ingredient.CHOCOLATE, Ingredient.CHOCOLATE, Ingredient.VANILLA, Ingredient.SUGAR),
            reward      = 180,
            time_limit  = 42.0,
            weight      = 6,
        ),
        CakeType.BUTTER_BOMB: Recipe(
            cake_type   = CakeType.BUTTER_BOMB,
            ingredients = (Ingredient.BUTTER, Ingredient.BUTTER, Ingredient.FLOUR, Ingredient.SUGAR),
            reward      = 110,
            time_limit  = 38.0,
            weight      = 6,
        ),
        CakeType.RAINBOW_MESS: Recipe(
            cake_type   = CakeType.RAINBOW_MESS,
            ingredients = (Ingredient.STRAWBERRY, Ingredient.VANILLA, Ingredient.CHOCOLATE, Ingredient.CREAM, Ingredient.EGG),
            reward      = 200,
            time_limit  = 44.0,
            weight      = 7,
        ),
        CakeType.CLOUD_CAKE: Recipe(
            cake_type   = CakeType.CLOUD_CAKE,
            ingredients = (Ingredient.CREAM, Ingredient.CREAM, Ingredient.SUGAR, Ingredient.VANILLA, Ingredient.FLOUR),
            reward      = 160,
            time_limit  = 50.0,
            weight      = 7,
        ),
        # --- Recettes rares (difficiles et récompenses élevées) ---
        CakeType.EGG_SURPRISE: Recipe(
            cake_type   = CakeType.EGG_SURPRISE,
            ingredients = (Ingredient.EGG, Ingredient.EGG, Ingredient.EGG, Ingredient.VANILLA, Ingredient.SUGAR),
            reward      = 220,
            time_limit  = 32.0,
            weight      = 3,
        ),
        CakeType.CURSED_TART: Recipe(
            cake_type   = CakeType.CURSED_TART,
            ingredients = (Ingredient.CHOCOLATE, Ingredient.STRAWBERRY, Ingredient.VANILLA, Ingredient.CREAM, Ingredient.EGG, Ingredient.BUTTER),
            reward      = 300,
            time_limit  = 35.0,
            weight      = 2,
        ),
    }

    @classmethod
    def get(cls, cake_type: CakeType) -> Recipe:
        return cls._recipes[cake_type]

    @classmethod
    def random(cls) -> Recipe:
        recipes  = list(cls._recipes.values())
        weights  = [r.weight for r in recipes]
        return random.choices(recipes, weights=weights, k=1)[0]

    @classmethod
    def all(cls) -> list:
        return list(cls._recipes.values())
