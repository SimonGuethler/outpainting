import os

from flask import Flask, send_file, render_template

from src.outpainting import outpainting
from src.utils import check_if_file_exists

app = Flask(__name__, template_folder='../html')


@app.route('/')
def index():
    return render_template('download.html')


@app.route('/download')
def download():
    # code to generate or retrieve file to download
    return send_file('../outpainting/image.png', as_attachment=True)


@app.route('/generate')
def generate():
    if check_if_file_exists("outpainting/image.png"):
        os.remove("outpainting/image.png")
    if check_if_file_exists("outpainting/prompts.txt"):
        os.remove("outpainting/prompts.txt")

    for _ in range(3):
        outpainting()

    return render_template('download.html')
