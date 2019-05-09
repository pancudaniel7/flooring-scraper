FROM python:3

RUN mkdir /app

COPY * /app
COPY resources /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "./src/main.py" ]