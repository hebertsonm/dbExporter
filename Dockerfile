FROM python:3.7.4-alpine3.9 AS build

RUN apk update \
    && apk add postgresql-client libffi-dev gcc musl-dev postgresql-dev
WORKDIR /dbExporter
ENV PATH=/root/.local/bin:$PATH
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

COPY src/ .

# Create image and copy requirements from build image. Also, install only
# essential packages for running the app. It reduces the image size 
# from 319 to 165 Mb
FROM python:3.7.4-alpine3.9 

RUN apk update && apk add postgresql-client
WORKDIR /dbExporter
COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application files at the end of building process to improve cache
COPY src/ .

ENTRYPOINT ["/usr/local/bin/python", "dbexporter.py"]
