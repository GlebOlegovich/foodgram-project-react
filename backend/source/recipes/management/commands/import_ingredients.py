import json
from tqdm import tqdm
import os

from django.core.management.base import BaseCommand

from ._settings_for_import import BASE_DIR, NEED_TO_PARSE
from ._core import insert_data_to_DB


class Command(BaseCommand):

    def _insert_data_to_DB(self, data, Model):
        valid_data = []
        new_items_count = 0

        # bulk-create не делает нумерацию pk
        obj_id = (
            Model.objects.latest('id').id + 1
            if Model.objects.all().exists()
            else 0
        )
        print('Проверяем, сколько элементов необходимо добавить в БД')
        
        for item in tqdm(data):
            obj =  Model.objects.filter(**item)
            if not obj.exists():
                valid_data.append(
                    Model(
                        id=obj_id,
                        **item
                    )
                )
                obj_id += 1
                new_items_count += 1
            # else:
            #     print(f'{obj} уже есть в модели {Model.__name__}' )

        if new_items_count > 0:
            print(
                f'В БД будет добавленно {new_items_count} элементов.\n'
                f'Они будут добавлены в модель {Model.__name__}'
            )
            Model.objects.bulk_create(
                valid_data,
                # Это максимум для SqLite
                batch_size=999
            )
            print(f'{Model.__name__} дополнены')
        else:
            print('Нет новых элементов, для добавления')


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
            Model = NEED_TO_PARSE[filename]
            )
