FROM python:3.9.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
COPY ./movies_admin/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
