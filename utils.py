import os


def save_image(image, folder, filename="image"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    files = os.listdir(folder)

    if len(files) > 0:
        last_file = files[-1]
        file_num = int(last_file.split(".")[0].split("_")[0]) + 1
    else:
        file_num = 0

    new_filename = str(file_num).zfill(4)

    image.save(f"{folder}/{new_filename}_{filename}.png")
