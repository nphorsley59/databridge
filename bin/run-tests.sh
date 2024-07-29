#!/bin/sh

# Ensure S3 bucket is available
echo "Waiting for S3 bucket to be available..."
while true; do
  echo "S3_ENDPOINT_URL: $S3_ENDPOINT_URL"
  echo "S3_BUCKET_NAME: $S3_BUCKET_NAME"
  echo "AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
  echo "AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
  echo "AWS_REGION: $AWS_REGION"
  echo "Running AWS CLI command to list S3 bucket..."
  output=$(aws --endpoint-url="$S3_ENDPOINT_URL" s3 ls)
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
echo "Waiting for Postgres databases to be available..."
while true; do
  echo "PG_USER: $PG_USER"
  echo "PG_HOST: $PG_HOST"
  echo "PG_PORT: $PG_PORT"
  echo "Running PSQL CLI command to list databases..."
  output=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -lqt | cut -d '|' -f 1 | grep -v '^$' | wc -l)
  if [ "$output" -gt 0 ]; then
    echo "There are $output databases available."
    break
  else
    echo "There are no databases available."
  fi
  sleep 10
done

# Run tests
echo "Running tests..."
poetry run pytest
