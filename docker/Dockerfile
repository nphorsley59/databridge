# Install Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install curl
RUN apt-get update && \
    apt-get install -y curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN arch=$(uname -m) && \
if [ "$arch" = "x86_64" ]; then \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"; \
elif [ "$arch" = "aarch64" ]; then \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"; \
else \
    echo "Unsupported architecture: $arch" && exit 1; \
fi && \
unzip awscliv2.zip && \
./aws/install && \
rm -rf awscliv2.zip aws

# Install PostgreSQL client utilities
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml poetry.lock pytest.ini ./ 
COPY databridge/ databridge/
COPY tests/ tests/
COPY docker/ docker/

# Create /scripts directory and copy the script
RUN mkdir -p /scripts
COPY bin/run-tests.sh /scripts/run-tests.sh

# Install Poetry and dependencies
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install

# Ensure shell scripts are executable
RUN chmod +x /scripts/run-tests.sh
