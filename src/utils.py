import os

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
