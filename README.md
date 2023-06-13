# Project Outpainting

> This repo consists of a pipeline to generate an infinite image from a newsfeed via stable diffusion inpainting.

## Docker

To start the docker container, run the following command

```bash
docker compose up -d
```

## Local Environment

### Installation

Install the Anaconda environment from the provided file

```bash
conda env create -f environment.yml
```

Set up the environment manually

```bash
conda create --name outpainting python=3.10
conda activate outpainting

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install --upgrade Flask
pip install --upgrade flask-cors
pip install --upgrade diffusers[torch]
pip install transformers
pip install accelerate
pip install waitress
pip install open-clip-torch
pip install newsapi-python
```

Activate the environment

```bash
conda activate outpainting
```

Add a huggingface token

```bash
huggingface-cli login --token $HUGGINGFACE_TOKEN
```

### Usage

#### Development

```bash
python flask-dev.py
```

#### Production

```bash
python serve.py
```

### Generation

Create an 'input' directory and add a file named 'prompts.json'.
The structure should look like that in the 'prompts.json.example'.

```bash
python generate.py
```

## Module Description

### ``aesthetic_predictor.py``

We use [LAION aesthetic predictor](https://github.com/LAION-AI/aesthetic-predictor) as quality assurance.
Each image gets rated after generation and based on that score we either take or throw away that image.

### ``app.py``

This file consists of a Flask API to serve the [Outpainting App](https://github.com/SimonGuethler/outpainting-app).

It also supports a small standalone page to control some functionality [localhost:8000](http://localhost:8000/).

### ``create_prompt.py``

We use news APIs to get the latest news headlines. This module handles that.

### ``database.py``

This module has a database class to connect to a local SQLite database.

### ``outpainting.py``

This is the heart of the project. It handles the outpainting process.

### ``outpainting_config.py``

The outpainting config can be found in the ``outpainting_config.ini`` file. This module handles that config.

### ``utils.py``

A collection of various different helper functions we use throughout the project.
