import os

from flask import Flask, send_file, render_template, Response, request
from flask_cors import CORS

from src.outpainting import outpainting
from src.utils import check_if_file_exists, read_text, get_image_path_for_index, build_complete_image, get_image_names

app = Flask(__name__, template_folder='../html')
CORS(app)


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

    image_path = get_image_path_for_index('outpainting', img_index)

    if not check_if_file_exists(image_path):
        return Response(status=404)

    return send_file(image_path, as_attachment=False)


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
    prompts_return = [i.strip() for i in parse if i != ""]
    return prompts_return


@app.route('/generate', methods=['GET'])
def generate():
    outpainting()

    return Response()


@app.route('/reset', methods=['GET'])
def reset():
    if check_if_file_exists("outpainting/image.png"):
        os.remove("outpainting/image.png")
    if check_if_file_exists("outpainting/prompts.txt"):
        os.remove("outpainting/prompts.txt")

    return Response()
