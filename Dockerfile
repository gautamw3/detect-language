FROM python:3.10-slim

RUN mkdir /opt/code

WORKDIR /opt/code

RUN apt-get update && apt-get install build-essential -y

COPY . .

RUN python3.10 -m venv env_langdetect
RUN env_langdetect/bin/pip install -U pip
RUN env_langdetect/bin/pip install wheel
RUN env_langdetect/bin/pip install -r requirements.txt

CMD ["env_langdetect/bin/python", "main.py"]
