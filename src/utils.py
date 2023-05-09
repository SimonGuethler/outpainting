import os
import re

from PIL import Image


def check_if_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def check_if_file_exists(path):
    return os.path.exists(path)


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


def save_image(image, folder, filename="image"):
    check_if_folder_exists(folder)

    image.save(f"{folder}/{filename}.png")


def read_image(path):
    if not check_if_file_exists(path):
        return None
    return Image.open(path)


def read_text(path):
    if not check_if_file_exists(path):
        return None
    with open(path, 'r') as file:
        return file.read()


def write_to_file(path, file, text, append=False):
    check_if_folder_exists(path)

    with open(f'{path}/{file}', 'a' if append else 'w') as file:
        file.write(text)


def save_image_batched(image, directory, filename="image"):
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


def read_image_batched(directory, filename="image"):
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