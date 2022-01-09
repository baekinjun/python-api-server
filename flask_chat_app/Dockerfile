# Base Image
FROM python:3.6

ENV PYTHONBUFFERED 1

# Set locale
ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Seoul

# Upgrading pip
RUN python -m pip install pip==21.0.1

RUN mkdir -p /api_chat

WORKDIR /api_chat

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get -o Dpkg::Options::='--force-confmiss' install --reinstall -y netbase

COPY . .

CMD ["gunicorn","-w" ,"1","--worker-class","eventlet", "-b" ,"0.0.0.0:5000" ,"--access-logfile","-" ,"--timeout","500" ,"--log-level","debug","chat:chat"]

