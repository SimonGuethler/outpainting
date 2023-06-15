FROM continuumio/anaconda3:latest

# Install base utilities
RUN apt-get update && apt-get install -y nano

# Set working directory
WORKDIR /app

# Create and activate the environment
RUN conda create --name outpainting python=3.10 && echo "conda activate outpainting" >> ~/.bashrc
ENV PATH /opt/conda/envs/outpainting/bin:$PATH

# Install dependencies
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch -c nvidia
RUN pip install --upgrade diffusers[torch] transformers accelerate Flask flask-cors waitress open-clip-torch newsapi-python

# Copy the project
COPY . .

# Expose port
EXPOSE 8000

# Set the entrypoint and default command
ENTRYPOINT ["conda", "run", "-n", "outpainting", "python", "serve.py"]
