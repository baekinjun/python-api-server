# Base Image
FROM python:3.6

ENV PYTHONBUFFERED 1

# Set locale
ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Seoul

# Upgrading pip
RUN python -m pip install pip==21.0.1

# Setup Folders
RUN mkdir -p /api_backend

# Move to working directory
WORKDIR /api_backend

COPY requirements.txt .
RUN pip install -r requirements.txt

#코드 복사
COPY . .
#uwsgi 실행
CMD ["gunicorn", "-w" ,"2", "-b" ,"0.0.0.0:8000" ,"--access-logfile","-" ,"--timeout","500" ,"-k" ,"gevent","--log-level","debug","wsgi:app"]


