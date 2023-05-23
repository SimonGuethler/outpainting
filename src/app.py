import os
import threading

from flask import Flask, send_file, render_template, Response, request
from flask_cors import CORS

from src.outpainting import Outpainting
from src.utils import check_if_file_exists, read_text, build_complete_image, get_image_names, \
    get_image_name_for_index

app = Flask(__name__, template_folder='../html', static_folder='../outpainting')
CORS(app)

generation_semaphore = threading.Semaphore()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/download', methods=['GET'])
def download():
    build_complete_image("outpainting")
    if not check_if_file_exists("outpainting/image.png"):
        return Response(status=404)
    return send_file('../outpainting/image.png', as_attachment=True)


@app.route('/image', methods=['GET'])
def image():
    img_index = request.args.get('img', default=0, type=int)

    image_filename = get_image_name_for_index('outpainting', img_index, input_schema=rf'^(\d+)_{"image"}\.webp$')

    if not image_filename:
        return Response(status=404)

    base_url = request.base_url
    base_url = base_url[:base_url.rfind('/') + 1]
    image_url = base_url + 'outpainting/' + image_filename

    return image_url


@app.route('/image_count', methods=['GET'])
def image_count():
    image_files = get_image_names('outpainting')
    return str(len(image_files))


@app.route('/prompts', methods=['GET'])
def prompts():
    prompts_input = read_text("outpainting/prompts.txt")
    if prompts_input is None:
        return Response(status=404)
    parse = prompts_input.split("\n")
    prompts_return = [i.strip() if index % 2 == 0 else "" for index, i in enumerate(parse) if i != ""]
    return prompts_return


@app.route('/generate', methods=['GET'])
def generate():
    count = request.args.get('count', default=1, type=int)
    generation_semaphore.acquire()
    outpainting = Outpainting()
    for _ in range(count):
        outpainting.generate_image()
    generation_semaphore.release()
    return Response()


@app.route('/reset', methods=['GET'])
def reset():
    image_files = get_image_names('outpainting')
    for file in image_files:
        os.remove(os.path.join('outpainting', file))

    if check_if_file_exists("outpainting/image.png"):
        os.remove("outpainting/image.png")
    if check_if_file_exists("outpainting/prompts.txt"):
        os.remove("outpainting/prompts.txt")

    return Response()
