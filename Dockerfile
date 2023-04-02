FROM python:3.10

# set working directory
WORKDIR /app

# install poetry
RUN pip install --upgrade pip \
    && pip install poetry

# copy files to working directory
COPY app /app/app
COPY tests /app/tests
COPY pyproject.toml poetry.lock /app/

# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--reload"]
