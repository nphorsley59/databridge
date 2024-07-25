#!/bin/sh

# Install AWS CLI
yum update -y
yum install -y aws-cli

# Wait for LocalStack to start
sleep 15

# Create the bucket
echo "Creating S3 bucket..."
aws --endpoint-url=http://localstack:4566 s3 mb s3://test-bucket --region us-east-1

# Verify the bucket creation
echo "Listing buckets to verify creation..."
aws --endpoint-url=http://localstack:4566 s3 ls