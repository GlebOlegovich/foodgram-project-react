# FROM python:3.9.5

# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt

FROM python:3.9.5

LABEL author='Godleib' version=1 broken_keyboards=5 pwd='/Users/mac/DEV/Yandex_prak/Production/FINAL'

WORKDIR /app
COPY /source .
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py makemigrations
CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
# CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000