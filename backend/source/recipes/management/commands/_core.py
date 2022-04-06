from tqdm import tqdm


def insert_data_to_DB(data, model):
    new_items_count = 0
    valid_data = []

    # bulk-create не делает нумерацию pk
    obj_id = (
        model.objects.latest('id').id + 1
        if model.objects.all().exists()
        else 0
    )
    print('Проверяем, сколько элементов необходимо добавить в БД')

    for item in tqdm(data):
        obj = model.objects.filter(**item)
        # Как еще тут ускориться я хз...
        # bulk_create не поддерживает функционал get_or_create
        if not obj.exists():
            valid_data.append(
                model(
                    id=obj_id,
                    **item
                )
            )
            obj_id += 1
            new_items_count += 1

    if new_items_count > 0:
        print(
            f'В БД будет добавленно {new_items_count} элементов.\n'
            f'Они будут добавлены в модель {model.__name__}'
        )
        model.objects.bulk_create(
            valid_data,
            # Это максимум для SqLite
            batch_size=999
        )
        print(f'{model.__name__} дополнены')
    else:
        print('Нет новых элементов, для добавления')
