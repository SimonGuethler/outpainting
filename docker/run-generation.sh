#!/bin/bash

# Build the Docker image
docker build -t outpainting_generate -f Dockerfile_custom ./outpainting

# Run the Docker container
docker run --rm \
  -v "$(pwd)/.cache:/root/.cache" \
  -v "$(pwd)/_output:/app/outpainting" \
  -v "$(pwd)/_export:/app/export" \
  -v "$(pwd)/_input:/app/input" \
  outpainting_generate
