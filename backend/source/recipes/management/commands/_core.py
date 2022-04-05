from tqdm import tqdm


def insert_data_to_DB(data, Model):
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
            # Как еще тут ускориться я хз...
            # bulk_create не поддерживает функционал get_or_create
            if not obj.exists():
                valid_data.append(
                    Model(
                        id=obj_id,
                        **item
                    )
                )
                obj_id += 1
                new_items_count += 1

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
