import json
import os

from django.core.management.base import BaseCommand

from ._core import insert_data_to_db
from ._settings_for_import import BASE_DIR, NEED_TO_PARSE


class Command(BaseCommand):

    def handle(self, *args, **options):
        for filename, model in NEED_TO_PARSE.items():
            print(
                f'Приступаем к заполнению {model}, данные берем из {filename}'
            )
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(BASE_DIR)),
                'initial_data'
            )
            json_file = os.path.join(data_dir, filename)
            with open(json_file, "r") as read_file:
                data = json.load(read_file)

            insert_data_to_db(
                data=data,
                model=model
            )
