FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/"

WORKDIR . /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libopencv-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "app.py", "8080"]
