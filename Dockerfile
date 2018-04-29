FROM python:3.6.5

# Making my life suck
LABEL Maintianer="Anish Gupta"

# Setting mode directory
RUN mkdir -p /home/app
WORKDIR /home/app
ENTRYPOINT [ "pipenv", "run", "python", "scheduler.py" ]

# Installing utils and deps
RUN apt-get update \
    && apt-get install -y gcc git python-dev \
    && apt-get clean
RUN pip install pipenv

COPY . /home/app
RUN pipenv install
