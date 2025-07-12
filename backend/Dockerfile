FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1