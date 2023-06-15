#!/bin/bash

# Build the Docker image
docker build -t stsiguet-outpainting-generate -f ./outpainting/Dockerfile_Generate ./outpainting

# Run the Docker container
docker run -d --rm --name stsiguet-outpainting-generate \
  --gpus 'device=0' \
  -v "$(pwd)/.cache:/root/.cache" \
  -v "$(pwd)/_output:/app/outpainting" \
  -v "$(pwd)/_export:/app/export" \
  -v "$(pwd)/_input:/app/input" \
  stsiguet-outpainting-generate
