FROM continuumio/anaconda3:latest

# Install base utilities
RUN apt-get update && \
    apt-get install -y nano && \
    apt-get autoremove && \
    apt-get clean

# Install the project
WORKDIR /app

## Create the environment
RUN conda create --name outpainting python=3.10

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "outpainting", "/bin/bash", "-c"]

# Init future bash with conda environment
RUN conda init bash
RUN echo "conda activate outpainting" >> ~/.bashrc

# Install dependencies
RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
RUN pip install --upgrade diffusers[torch]
RUN pip install transformers
RUN pip install accelerate
RUN pip install --upgrade Flask
RUN pip install --upgrade flask-cors
RUN pip install waitress
RUN pip install open-clip-torch
RUN pip install newsapi-python

# Copy the project
COPY . .

EXPOSE 8000
CMD bash -C 'serve.sh';'bash'
#ENTRYPOINT ["tail", "-f", "/dev/null"]
