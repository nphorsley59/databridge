# Install Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY databridge/ databridge/
COPY tests/ tests/
COPY docker/ docker/

# Install Poetry and dependencies
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install

# Run tests
CMD ["poetry", "run", "pytest"]
