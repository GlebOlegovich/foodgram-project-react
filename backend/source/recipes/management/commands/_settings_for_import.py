import os

from recipes.models import Ingredient
from config.settings import BASE_DIR

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(BASE_DIR)),
    'data'
)

NEED_TO_PARSE = {
    'ingredients.json': Ingredient,
}
