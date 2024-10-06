# Use a base Python image
FROM python:3.10-alpine3.14
LABEL maintainer="metalbrain.net"

ENV PYTHONDONTWRITEBYTECODE=1

COPY ./dev-requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Set the working directory in the container
COPY ./app /app
WORKDIR /app
# Expose the Flask port
EXPOSE 5000
ARG DEV=false
# Install Python dependencies
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  apk add --update --no-cache postgresql-client && \
  apk add --update --no-cache --virtual .tmp-build-deps \ 
  build-base postgresql-dev musl-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ $DEV = "true" ]; \
  then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  adduser \
  --disabled-password \
  --no-create-home \
  django-user

ENV PATH="/py/bin:$PATH"
# Switch to the non-root user
USER django-user





