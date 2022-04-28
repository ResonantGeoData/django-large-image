FROM python:3.9-slim as build
COPY setup.py /opt/build-context/setup.py
COPY MANIFEST.in /opt/build-context/MANIFEST.in
COPY ./django_large_image/ /opt/build-context/django_large_image
WORKDIR /opt/build-context
RUN python -m pip install --upgrade pip wheel setuptools
RUN python setup.py sdist bdist_wheel


FROM ghcr.io/girder/large_image:latest as myimages
# Install system libraries for Python packages:
# * psycopg2
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
        libpq-dev gcc libc6-dev \
        && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=build /opt/build-context/dist/*.whl /opt/django-project/wheels/

RUN pip install --find-links https://girder.github.io/large_image_wheels \
  $(ls -1  /opt/django-project/wheels/*.whl) \
  gunicorn

COPY ./myimages/ /opt/django-project
# Use a directory name which will never be an import name, as isort considers this as first-party.
WORKDIR /opt/django-project

RUN /opt/django-project/manage.py migrate
RUN /opt/django-project/manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]
# ENTRYPOINT ["gunicorn", "-k", "gthread", "--threads", "8", "--bind", "0.0.0.0:8000", "myimages.wsgi"]
