FROM python:3.12

RUN mkdir /servicename

WORKDIR /servicename

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .