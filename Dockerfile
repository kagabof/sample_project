FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin
RUN mkdir /hashes_apps
WORKDIR /hashes_apps

RUN pip install --upgrade pip

ADD requirements.txt /hashes_apps/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /hashes_apps/

EXPOSE 8000
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app", "--timeout", "1000"]
