FROM python:3.10-slim

# set working directory
WORKDIR /app

# copy requirements file to work directory
COPY pyproject.toml poetry.lock ./

# install poetry
RUN pip install --upgrade pip \
    && pip install poetry

# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application to the container
COPY app ./app
COPY tests ./tests

# run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
