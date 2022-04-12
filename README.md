![example workflow](https://github.com/GlebOlegovich/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

# Проект Foodgram «Продуктовый помощник»
![Image](https://raw.githubusercontent.com/GlebOlegovich/foodgram-project-react/Developing/preview.png)

В проекте настроены [[GitHub Actions]](#GitHub-Actions), которые позволяют использовать все прелести ```CI/CD```

## Описание
Кулинарный онлайн-сервис и API для него.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок, необходимых для приготовления выбранных блюд и скачивать его в PDF формате.
#### Сайт доступен по адресу http://foodgram.gudleifr.ru/
#### Полная документация по API: http://foodgram.gudleifr.ru/api/docs/
[[Зависимости для backend]](https://github.com/GlebOlegovich/foodgram-project-react/blob/master/backend/requirements.txt)

### Пример функционала админ зоны
#### Админка: http://foodgram.gudleifr.ru/admin
#### Данные для доступа
- Username: admin
- Password: admin
- Email: admin@example.com

:one: Все модели доступны в админ-зоне, в том числе редактирование/удаление записей.

:two: На админ-странице рецепта отображается количество добавлений этого рецепта в избранное.

:three: Для модели ингредиентов включена фильтрация по названию.

## Создание пользователя администратором
Пользователя может создать администратор — через админ-зону или через POST-запрос на специальный эндпоинт ```api/users/```

Получение токена авторизации реализовано через отправку POST-запроса с параметрами email и password на эндпоинт ```/api/auth/token/```. Далее этот токен передается в хэдере запроса, например : ```Authorization : Token 207881e50_..._94d55778```.

## Пользовательские роли
| Функционал                                                                                                                | Неавторизованные пользователи |  Авторизованные пользователи | Администратор  |
|:--------------------------------------------------------------------------------------------------------------------------|:---------:|:---------:|:---------:|
| Доступна главная страница.                                                                                                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма авторизации                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница отдельного рецепта.                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма регистрации.                                                                                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Мои подписки»                                                                                          | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице рецепта                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице автора                                                                         | :x: | :heavy_check_mark: | :heavy_check_mark: |
| При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Избранное»                                                                                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда           | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Список покупок»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда              | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок» | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Создать рецепт»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность опубликовать свой рецепт                                                                                 | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность отредактировать и сохранить изменения в своём рецепте                                                    | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность удалить свой рецепт                                                                                      | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма изменения пароля                                                                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна возможность выйти из системы (разлогиниться)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Изменять пароль любого пользователя.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Создавать/блокировать/удалять аккаунты пользователей.                                                                     | :x: | :x: | :heavy_check_mark: |
| Редактировать/удалять любые рецепты.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать ингредиенты.                                                                              | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать теги.                                                                                     | :x: | :x: | :heavy_check_mark: |


## Запуск проекта на сервере
:zero: Подключиться к серверу по ```ssh```
:video_game: ```ssh USER_SERVER@HOST_SERVER```

:one: Настроить сервер, для работы с [[git]](https://andreyex.ru/operacionnaya-sistema-linux/kak-nastroit-git-server-na-linux/) и [[docker-compose]](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru).

:two: Выгрузить ```initial_data``` на сервер
#### Пример выгрузки папки initial_data, на сервер
``` scp -r initial_data/ USER_SERVER@HOST_SERVER:apps/foodgram-project-react/ ```

:three::information_source::one: Клонировать весь репозиторий [[репозиторий]](https://github.com/GlebOlegovich/foodgram-project-react), в этом случае можно внести изменения в ```docker-compose.yml```, что бы вместо взятия образа с DockerHub, происходил бы билд с локальной версии.

:vs:

:three::information_source::two: Скачать и загрузить на сервер папку [[infra]](https://github.com/GlebOlegovich/foodgram-project-react/tree/master/infra), в этом случае образы для docker-compose подхватятся с DockerHub.

#### Клонировать репозиторий на сервер
```git clone https://github.com/GlebOlegovich/foodgram-project-react.git```

:shipit: or

```git clone git@github.com:GlebOlegovich/foodgram-project-react.git```


#### Далее будет рассматриваться :three::information_source::two:случай.

:four: Переходим в дирректорию :books: ```infra```.

Конфигрурируем ```.env```, пример:
```
SECRET_KEY=insert_key
# указываем, что работаем с postgresql
# DB_ENGINE=django.db.backends.postgresql
DB_ENGINE=django.db.backends.postgresql

# имя базы данных
# DB_NAME=postgres
DB_NAME=postgres

# логин для подключения к базе данных
# POSTGRES_USER=postgres
POSTGRES_USER=postgres

# пароль для подключения к БД (установите свой)
# POSTGRES_PASSWORD=postgres
POSTGRES_PASSWORD=postgres

# название сервиса (контейнера)
# DB_HOST=db
DB_HOST=db

# порт для подключения к БД
# DB_PORT=5432
DB_PORT=5432
```

:five: Запускаем контейнеры, находясь в дирректорию :books: ```infra``` : ```sudo docker-compose up -d```

:six: Внутри контейнера ```backend``` выполнить миграции, собирать статику и выгрузить первичные данные [[impirt_initial_data]](#Managment-comands)

Подключаемся к контейнеру backend:
```sudo docker-compose exec -T backend sh```
Внутри него выполняем следующие действия:
```
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py impirt_initial_data
```
:eight:
    Для скачивания PDF списка покупок:
    [Это уже прописано в докерфайле в backend](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#ubuntu-20-04), но продублируем еще и сюда)
    
    ```apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0```

### Managment-comands:
```python manage.py impirt_initial_data``` - залить в БД ингридиенты,теги итп. Данные должны быть в json формате, назфание файла и модель, в которой будут делаться записи должны быть указаны в ```foodgram-project-react/backend/source/recipes/management/commands/_settings_for_import.py```.

Расположение данных - директория initial_data (на уровне с дирректорией всего проекта (source) - ```foodgram-project-react/initial_data```).

## Запуск в DEV режиме:
```docker-compose -f docker-compose_dev.yml up```

```python manage.py runserver```

В контейнере будут запущены: postgres, nginx, frontend. Backend будет рабоать локально. 

Что бы работал рендеринг PDF - [установим необходимые приложения](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#macos) :
```brew install python pango libffi```
```
python3 -m venv venv
source venv/bin/activate
pip install weasyprint
weasyprint --info
```

Мануал, по использованию weasyprint: [href](https://www.youtube.com/watch?v=_zkYICsIbXI&t=674s)

## GitHub-Actions
Если внести любые изменения в проект и выполнить:
```
git add .
git commit -m "..."
git push
```
Комманда git push является триггером workflow проекта (при пуше в ветку Developing/Production - workflow отличаются). При выполнении команды git push запустится набор блоков комманд jobs. Выполняются следующие блоки:

- tests - тестирование проекта на соответствие PEP8 и тестам pytest.

- build_and_push_to_docker_hub - при успешном прохождении тестов собирается образ (image) для docker контейнера и отправлятеся в DockerHub

- deploy - после отправки образа на DockerHub начинается деплой проекта на сервере. 

- send_message - после сборки и запуска контейнеров происходит отправка сообщения в телеграм об успешном окончании workflow. (В случае каких либо ошибок, отправляется оповешение об ошибках)

# Контакты автора проекта:
_Глеб Олегович_
---
**email:** _i@godleib.ru_  
**telegram:** _@GodLeib_  
