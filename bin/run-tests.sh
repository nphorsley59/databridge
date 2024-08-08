#!/bin/sh

# Wait for other services to spin up
echo "Pausing to allow test-dependent services to spin up..."
sleep 30

# Ensure S3 bucket is available
echo "Checking if S3 bucket is available..."
while true; do
  echo "AWS_ENDPOINT_URL: $AWS_ENDPOINT_URL"
  echo "S3_BUCKET_NAME: $S3_BUCKET_NAME"
  echo "AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
  echo "AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
  echo "AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION"
  echo "Running AWS CLI command..."
  output=$(aws --endpoint-url="$AWS_ENDPOINT_URL" s3 ls)
  echo "Available buckets: $output"
  if echo "$output" | grep -q "test-bucket"; then
    echo "S3 bucket $S3_BUCKET_NAME is available."
    break
  else
    echo "S3 bucket $S3_BUCKET_NAME is not available yet."
  fi
  sleep 10
done

# Ensure Postgres database is available
echo "Checking if Postgres database is available..."
while true; do
  echo "POSTGRES_USER: $POSTGRES_USER"
  echo "POSTGRES_HOST: $POSTGRES_HOST"
  echo "POSTGRES_PORT: $POSTGRES_PORT"
  echo "POSTGRES_DB: $POSTGRES_DB"
  echo "Running PSQL CLI command..."
  output=$(psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
  if [ "$output" = "1" ]; then
    echo "Database $POSTGRES_DB is available."
    break
  else
    echo "Database $POSTGRES_DB is not available."
  fi
  sleep 10
done

# Run tests
echo "Running tests..."
poetry run pytest
