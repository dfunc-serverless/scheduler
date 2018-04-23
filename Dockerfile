FROM python:3.6.5

# Making my life suck
LABEL Maintianer="Anish Gupta"

# Exposing endpoint port
EXPOSE 8888

# Setting mode directory
RUN mkdir -p /home/app
COPY . /home/app
WORKDIR /home/app

# Installing utils and deps
RUN apt update && apt install -y gcc git python-dev
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "scheduler.py" ]