# Порядок работы с контейнером:

# IMAGE контейнера придётся собрать
# из корня проекта:
#           $ docker build web_app

# Запустить командой:
#           $ docker run -p 5000:5000 web-app

# при запуске можно задать имя контейнера
#           $ docker run --name=somename -p 5000:5000 web-app

# Поделка будет доступна по адресу 127.0.0.1/5000

# Как надоест, Flask останавливается 'Ctrl-C'

# Не знаю как у кого, у меня коинтейнер сам не останавливается поэтому практически полезно использовать:

#           $ docker ps

# покажет запущенные контейнеры
# Результат может быть примерно таким:

# CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS          PORTS                                       NAMES
# 91edc03647e5   web-app   "flask run --host=0.…"   About a minute ago   Up 55 seconds   0.0.0.0:5050->5000/tcp, :::5050->5000/tcp   wonderful_dirac
# 53592a6f72b7   web-app   "flask run --host=0.…"   4 minutes ago        Up 3 minutes    0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   keen_maxwell

# Откуда берутся эти дурацкие имена я не знаю, но контейнеры доступны по этим именам или по ID:

# Заглянуть в запущенный контейнер можно командой:
#           $ docker exec -it [CONTAINER ID] bash
# Для счастливых обладателей Винды:
#           $ winpty docker exec -it [CONTAINER ID] bash

# Командой '$ docker stop [CONTAINER ID]

#           $ docker stop 91edc03647e5 или ($docker stop wonderful_dirac)
#           $ docker stop 53592a6f72b7 или ($docker stop wonderful_dirac)

# если имя задано то '$docker stop somename'
# или

#           $ docker stop $(docker ps -a -q)

# это остановит все запущенные контейнеры
# потом всё это можно удалить:

#           $ docker rm $(docker ps -a -q)

# и проверить не осталось ли чего:

#           $ docker ps --all

# покажет все контейнеры, запущенные и остановленные
# а можно не удалять, и стартовать по имени:
#           $ docker start somename


FROM python:3.9.5-buster

WORKDIR /app

RUN pip install -U pip setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY __init__.py .
COPY app.py .

COPY templates templates


ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
