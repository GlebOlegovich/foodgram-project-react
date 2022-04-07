# praktikum_new_diplom

Первый этап - 09.03.2022

Отправка на второе ревью первого этапа - 06.04.2022 (Брал академ, времени было мало на проект, поэтому только сейчас)

На первом этапе проверяется весь код проекта (включая файл зависимостей requirements.txt).

После проверки кода ревьюер прокомментирует вашу работу: укажет, что нужно поправить или сообщит, что всё ОК и можно переходить ко второму этапу.

## Managment comands:
```python manage.py impirt_initial_data``` - залить в БД ингридиенты,теги итп. Данные должны быть в json формате, назфание файла и модель, в которой будут делаться записи должны быть указаны в ```foodgram-project-react/backend/source/recipes/management/commands/_settings_for_import.py```. Расположение данных - директория data (на уровне с дирректорией всего проекта (source) - ```foodgram-project-react/data```).

## Запуск в DEV режиме:
docker-compose -f docker-compose_dev.yml up и python manage.py runserver