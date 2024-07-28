#!/bin/sh

# Ensure S3 bucket is available
echo "Waiting for S3 bucket to be available..."
while true; do
  echo "S3_AWS_ENDPOINT_URL: $S3_AWS_ENDPOINT_URL"
  echo "S3_AWS_BUCKET_NAME: $S3_AWS_BUCKET_NAME"
  echo "AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
  echo "AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
  echo "Running AWS CLI command to list S3 bucket..."
  output=$(aws --endpoint-url="$S3_AWS_ENDPOINT_URL" s3 ls)
  echo "Available buckets: $output"
  if echo "$output" | grep -q "test-bucket"; then
    echo "S3 bucket $S3_AWS_BUCKET_NAME is available."
    break
  else
    echo "S3 bucket $S3_AWS_BUCKET_NAME is not available yet."
  fi
  sleep 5
done

# Run tests
echo "Running tests..."
poetry run pytest
