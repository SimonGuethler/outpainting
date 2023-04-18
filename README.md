# Project Outpainting

> This repo consists of a pipeline to generate an infinite image from a newsfeed via stable diffusion inpainting.

## Installation

Install the Anaconda environment from the provided file

```bash
conda create --name outpainting --file environment.yml
```

Set up the environment manually

```bash
conda create --name outpainting python=3.10

conda install -c conda-forge diffusers
conda install -c conda-forge transformers
conda install -c conda-forge accelerate
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

Activate the environment

```bash
conda activate outpainting
```

Add a huggingface token

```bash
huggingface-cli login --token $HUGGINGFACE_TOKEN
```

Add NYTimes API-keys:

1. create account and generate keys: https://developer.nytimes.com/apis
2. add keys to "config.ini"

## Usage

### Single Image

```bash
python single_image.py
```
