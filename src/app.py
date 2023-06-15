import threading

from flask import Flask, send_file, render_template, Response, request
from flask_cors import CORS

from src.database import Database
from src.outpainting import Outpainting
from src.utils import check_if_file_exists, build_complete_image, get_image_names, check_if_folder_exists, reset_folder

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

    db = Database()
    db_entry = db.get_entry_by_id(img_index)
    db.close_connection()

    if not db_entry:
        return Response(status=404)

    image_filename = db_entry.image + '.webp',

    if not image_filename:
        return Response(status=404)

    base_url = request.base_url
    base_url = base_url[:base_url.rfind('/') + 1]
    image_url = base_url + 'outpainting/' + image_filename

    return image_url


@app.route('/images', methods=['GET'])
def images():
    image_files = get_image_names('outpainting')
    if len(image_files) == 0:
        return Response(status=404)

    base_url = request.base_url
    base_url = base_url[:base_url.rfind('/') + 1]
    image_urls = [base_url + 'outpainting/' + file for file in image_files]

    return image_urls


@app.route('/data', methods=['GET'])
def data():
    check_if_folder_exists("outpainting")

    db = Database()
    db_entries = db.get_all_entries()
    db.close_connection()

    if len(db_entries) == 0:
        return Response(status=404)

    base_url = request.base_url
    base_url = base_url[:base_url.rfind('/') + 1]

    result = []
    for entry in db_entries:
        result.append({
            "image": base_url + 'outpainting/' + entry.image + '.webp',
            "prompt": entry.prompt.strip(),
            "headline": entry.headline.strip(),
            "source": entry.source.strip(),
            "date": entry.date.strip()
        })

    return result


@app.route('/image_count', methods=['GET'])
def image_count():
    image_files = get_image_names('outpainting')
    return str(len(image_files))


@app.route('/prompts', methods=['GET'])
def prompts():
    db = Database()
    db_entries = db.get_all_entries()
    db.close_connection()

    if len(db_entries) == 0:
        return Response(status=404)

    prompts_return = [i.prompt.strip() for i in db_entries if i != ""]
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
    generation_semaphore.acquire()

    db = Database()
    db.delete_all_entries()
    db.close_connection()

    reset_folder("outpainting")

    generation_semaphore.release()
    return Response()
