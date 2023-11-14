# Dockerfile for app stack installation
FROM python:3.9.18-slim

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

EXPOSE 2020
CMD ["python3",  "/code/app.py"]
