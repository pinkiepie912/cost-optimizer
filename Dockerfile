FROM python:3.9-slim-buster

#
# SET ENV
#
ENV ROOT_DIR=/app 
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

#
# INSTALL DEPENDENCIES
#
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install apt-utils \
    build-essential \
    gcc \
    curl

#
# SET WORKDIR
#
WORKDIR ${ROOT_DIR} 

#
# COPY FILES
#
COPY . ${ROOT_DIR} 

#
# INSTALL POETRY
#
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false --local
RUN poetry install --no-interaction --no-ansi --no-root

#
# Lambda Runtime Interface Client
#
RUN poetry add awslambdaric

ENTRYPOINT ["python3", "-m", "awslambdaric"]
CMD ["src.main"]
