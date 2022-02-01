#
FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/"

#
WORKDIR . /app

#
COPY requirements.txt requirements.txt


RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        libopencv-dev \
        build-essential \
        libssl-dev \
        libpq-dev \
        libcurl4-gnutls-dev \
        libexpat1-dev \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
#

RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install opencv-contrib-python

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt


#
COPY . .

#
CMD ["python", "main.py", "8080"]