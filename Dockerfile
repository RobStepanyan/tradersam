FROM python:latest
ADD . /tradersam
WORKDIR /tradersam
COPY . /tradersam/
COPY requirements.txt /tradersam/
RUN pip install -r requirements.txt
