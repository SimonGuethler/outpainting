import os
import re
from datetime import datetime

from PIL import Image

from src.database import Database

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_if_folder_exists(folder):
    os.makedirs(folder, exist_ok=True)


def check_if_file_exists(path) -> bool:
    return path and os.path.exists(path)


def save_image_series(image, folder, filename="image"):
    check_if_folder_exists(folder)

    files = os.listdir(folder)

    if len(files) > 0:
        last_file = files[-1]
        file_num = int(last_file.split(".")[0].split("_")[0]) + 1
    else:
        file_num = 0

    new_filename = str(file_num).zfill(4)

    image.save(f"{folder}/{new_filename}_{filename}.png")


def save_image(image, folder, filename="image") -> str:
    check_if_folder_exists(folder)

    filename = f'{filename}.png'
    image.save(os.path.join(folder, filename))
    return filename


def read_image(path) -> Image or None:
    if not check_if_file_exists(path):
        return None
    return Image.open(path)


def read_text(path) -> str or None:
    if not check_if_file_exists(path):
        return None
    with open(path, 'r') as file:
        return file.read()


def write_to_file(path, file, text, append=False):
    check_if_folder_exists(path)

    with open(f'{path}/{file}', 'a' if append else 'w') as file:
        file.write(text)


def save_image_batched(image, directory, filename="image") -> str:
    check_if_folder_exists(directory)
    files = os.listdir(directory)

    latest_file_int = 0
    for file in files:
        match = re.search(rf'^(\d+)_{filename}\.png$', file)
        if match:
            i = int(match.group(1))
            if i > latest_file_int:
                latest_file_int = i

    filename = f'{latest_file_int + 1:04}_{filename}.png'
    image.save(os.path.join(directory, filename))
    return filename


def read_image_batched(directory, filename="image") -> Image or None:
    check_if_folder_exists(directory)
    files = os.listdir(directory)

    latest_file_int = 0
    latest_filename = None
    for file in files:
        match = re.search(rf'^(\d+)_{filename}\.png$', file)
        if match:
            i = int(match.group(1))
            if i > latest_file_int:
                latest_file_int = i
                latest_filename = file

    if latest_filename is not None:
        return Image.open(os.path.join(directory, latest_filename))
    else:
        return None


def get_image_names(directory, input_schema=rf'^(\d+)_{"image"}\.png$') -> list[str]:
    check_if_folder_exists(directory)
    return sorted(
        [file for file in os.listdir(directory) if re.search(input_schema, file)])


def build_complete_image(directory, input_schema=rf'^(\d+)_{"image"}\.png$', output_image_name="image",
                         image_extension='.png') -> Image or None:
    image_files = sorted(
        [file for file in os.listdir(directory) if file.endswith(image_extension) and re.search(input_schema, file)])

    if len(image_files) == 0:
        return None

    first_image = Image.open(os.path.join(directory, image_files[0]))
    width, height = first_image.size

    concatenated_image = Image.new('RGB', (width * len(image_files), height))

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)
        concatenated_image.paste(image, (i * width, 0))

    concatenated_image.save(os.path.join(directory, output_image_name + image_extension))

    first_image.close()
    return concatenated_image


def get_image_path_for_index(directory, index=0, input_schema=rf'^(\d+)_{"image"}\.png$') -> str or None:
    complete_path: str = os.path.join(ROOT_DIR, directory)
    image_files = sorted(
        [file for file in os.listdir(complete_path) if re.search(input_schema, file)])

    if len(image_files) == 0 or index >= len(image_files):
        return None

    return os.path.join(complete_path, image_files[index])


def get_image_name_for_index(directory, index=0, input_schema=rf'^(\d+)_{"image"}\.png$') -> str or None:
    complete_path: str = os.path.join(ROOT_DIR, directory)
    image_files = sorted(
        [file for file in os.listdir(complete_path) if re.search(input_schema, file)])

    if len(image_files) == 0 or index >= len(image_files):
        return None

    return image_files[index]


def get_image_for_index(directory, index=0, input_schema=rf'^(\d+)_{"image"}\.png$',
                        image_extension='.png') -> Image or None:
    complete_path: str = os.path.join(ROOT_DIR, directory)
    image_path = get_image_path_for_index(complete_path, index, input_schema, image_extension)
    if image_path is None:
        return None
    return Image.open(image_path)


def is_in_file(path, file, string):
    string = string.lower()
    if check_if_file_exists(f'{path}/{file}'):
        with open(f'{path}/{file}', 'r') as read_obj:
            for line in read_obj:
                if string in line.lower():
                    return True
    return False


def convert_img_to_webp(input_path, quality=80):
    if not check_if_file_exists(input_path):
        return

    image = Image.open(input_path)
    output_path = input_path.split(".")[0] + ".webp"
    image.save(output_path, "WebP", quality=quality)


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_first_new_prompt(data: dict) -> str:
    if len(data['prompts']) == 0:
        return ""

    db = Database()
    db_entries = db.get_all_entries()
    db.close_connection()

    if len(db_entries) == 0:
        return data['prompts'][0], data['headlines'][0], data['sources'][0], data['dates'][0]

    for i, prompt in enumerate(data['prompts']):
        if prompt not in [e.prompt for e in db_entries]:
            return data['prompts'][i], data['headlines'][i], data['sources'][i], data['dates'][i]

    return '', '', '', ''
