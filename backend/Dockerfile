FROM python:3.8-slim as test

# dependencies
COPY requirements-test.txt /db-experiment/
WORKDIR /db-experiment
RUN pip install -r requirements-test.txt

# source
COPY . /db-experiment

ENTRYPOINT coverage run -m pytest && coverage html

# run stage
FROM python:3.8-slim as run

# dependencies
COPY requirements-run.txt /db-experiment/
WORKDIR /db-experiment
RUN pip install -r requirements-run.txt

# source 
COPY app /db-experiment/app
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]