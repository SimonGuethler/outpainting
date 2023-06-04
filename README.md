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
