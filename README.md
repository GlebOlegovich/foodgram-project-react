# praktikum_new_diplom

Первый этап - 09.03.2022

Отправка на второе ревью первого этапа - 06.04.2022 (Брал академ, времени было мало на проект, поэтому только сейчас)

На первом этапе проверяется весь код проекта (включая файл зависимостей requirements.txt).

После проверки кода ревьюер прокомментирует вашу работу: укажет, что нужно поправить или сообщит, что всё ОК и можно переходить ко второму этапу.

## Managment comands:
```python manage.py import_ingredients``` - залить в БД ингридиенты, данные должны быть в json формате, назфание файла - ingredients.json. Расположение - директория data.

## Запуск в DEV режиме:
docker-compose -f docker-compose_dev.yml up и python manage.py runserver