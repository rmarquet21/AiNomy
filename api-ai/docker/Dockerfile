FROM python:3.8

WORKDIR /app

ADD requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . /app

RUN alfred download:model:pneumonia
RUN alfred download:model:alzheimer

CMD ["/bin/bash", "-c", "alfred datastore:init;alfred datastore:upgrade;alfred run:web:gunicorn"]
