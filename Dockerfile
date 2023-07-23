FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 80

ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal postgresql-client libgdal-dev
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=usr/include/gdal

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


RUN mkdir -p /docker-entrypoint-initdb.d

CMD ["gunicorn", "reporter.wsgi", ":80"]