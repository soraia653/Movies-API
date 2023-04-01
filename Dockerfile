FROM python:3.10

# set working directory
WORKDIR /app

# install poetry
RUN pip install poetry

# copy files to working directory
COPY ./app /app
COPY pyproject.toml /app

# set up poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 python3 -
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--reload"]