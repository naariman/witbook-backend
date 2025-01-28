FROM python:3.8.3-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    zlib-dev \
    jpeg-dev \
    libffi-dev \
    openssl-dev

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["gunicorn", "witbook.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]