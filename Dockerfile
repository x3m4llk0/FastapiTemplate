FROM python:3.12

RUN mkdir /templateservice

WORKDIR /templateservice

COPY requirements.txt .
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .