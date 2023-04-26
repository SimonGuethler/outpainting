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
RUN pip install --upgrade Flask
RUN pip install --upgrade diffusers[torch]
RUN pip install transformers
RUN pip install accelerate

# Copy the project
COPY ./src ./src
COPY config.ini .
COPY run.py .

#EXPOSE 8000
#ENTRYPOINT ["python", "run.py"]
#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["tail", "-f", "/dev/null"]
