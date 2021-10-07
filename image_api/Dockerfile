FROM python:3.9.7-alpine

WORKDIR /app
COPY ./requirements.txt /app
COPY . /app

RUN apk --update add \
    gcc\
    build-base \
    jpeg-dev\
    zlib-dev


RUN python3 -m pip install --upgrade pip 
RUN python3 -m pip install -r requirements.txt



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
