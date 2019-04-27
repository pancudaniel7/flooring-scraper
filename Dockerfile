FROM python:3

RUN mkdir /app

COPY resources/ /app
COPY src/ /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "./src/main.py" ]