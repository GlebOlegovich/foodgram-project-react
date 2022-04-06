import json
import os

from django.core.management.base import BaseCommand

from ._core import insert_data_to_DB
from ._settings_for_import import BASE_DIR, NEED_TO_PARSE


class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'ingredients.json'
        DATA_DIR = os.path.join(
            os.path.dirname(os.path.dirname(BASE_DIR)),
            'data'
        )
        json_file = os.path.join(DATA_DIR, filename)
        with open(json_file, "r") as read_file:
            data = json.load(read_file)

        insert_data_to_DB(
            data=data,
            model=NEED_TO_PARSE[filename]
        )
