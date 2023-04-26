#FROM python:3.10-slim-buster
FROM continuumio/anaconda3:latest

# Install base utilities
RUN apt-get update && \
#    apt-get install -y build-essentials  && \
#    apt-get install -y wget && \
    apt-get install -y nano && \
    apt-get autoremove && \
    apt-get clean

## Install miniconda
#ENV CONDA_DIR /opt/conda
#RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p /opt/conda
#
## Put conda in path so we can use conda activate
#ENV PATH=$CONDA_DIR/bin:$PATH


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


#FROM continuumio/miniconda3:4.12.0
#
#RUN apt-get update && \
#    apt install -y \
#      fonts-dejavu-core  \
#      build-essential \
#      libopencv-dev \
#      cmake \
#      vim \
#      && apt-get clean
#
#COPY docker/opencv.pc /usr/lib/pkgconfig/opencv.pc
#
#RUN useradd -ms /bin/bash user
#USER user
#
#RUN mkdir ~/.huggingface && conda init bash
#
#COPY --chown=user:user . /app
#WORKDIR /app
#
#EXPOSE 8888
#CMD ["/app/docker/entrypoint.sh"]
