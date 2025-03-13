FROM python:3.12
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root --no-interaction
COPY backend /app
RUN poetry run pip install uvicorn
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
