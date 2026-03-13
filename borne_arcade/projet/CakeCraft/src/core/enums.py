from enum import Enum

class MenuButton(Enum):
    JOUER   = "Jouer"
    SCORE   = "Score"
    QUITTER = "Quitter"

class Side(Enum):
    LEFT  = "left"
    RIGHT = "right"

class Ingredient(Enum):
    FLOUR      = "Farine"
    EGG        = "Oeuf"
    BUTTER     = "Beurre"
    SUGAR      = "Sucre"
    CREAM      = "Crème"
    CHOCOLATE  = "Chocolat"
    STRAWBERRY = "Fraise"
    VANILLA    = "Vanille"

class CakeType(Enum):
    VANILLA_CAKE       = "Gâteau Vanille"
    CHOCOLATE_CAKE     = "Gâteau Chocolat"
    STRAWBERRY_CAKE    = "Gâteau Fraise"
    CREAM_PUFF         = "Chou à la Crème"
    CHEWING_GUM_CAKE   = "Gâteau Chewing-Gum"
    BUTTER_BOMB        = "Bombe au Beurre"
    EGG_SURPRISE       = "Surprise à l'Oeuf"
    RAINBOW_MESS       = "Chaos Arc-en-Ciel"
    CURSED_TART        = "Tarte Maudite"
    CLOUD_CAKE         = "Gâteau Nuage"

class CustomerState(Enum):
    WALKING  = "walking"
    QUEUED   = "queued"
    WAITING  = "waiting"
    SERVED   = "served"
    LEAVING  = "leaving"

class GameState(Enum):
    PLAYING = "playing"
    LOST    = "lost"

class DeliveryResult(Enum):
    SUCCESS     = "success"
    NO_CUSTOMER = "no_customer"
    WRONG_ITEM  = "wrong_item"
    WRONG_ORDER = "wrong_order"
    NOT_COOKED = "not_cooked"
