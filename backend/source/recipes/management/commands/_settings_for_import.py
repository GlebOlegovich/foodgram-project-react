import os

from config.settings import BASE_DIR
from recipes.models import Ingredient

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(BASE_DIR)),
    'data'
)

NEED_TO_PARSE = {
    'ingredients.json': Ingredient,
}
