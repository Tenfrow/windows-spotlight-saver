import os
import sys
from PIL import Image
from shutil import copyfile
from time import time

source_path = os.path.join(os.getenv('LOCALAPPDATA'),
                           r'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')

dest_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spotlight')

if not os.path.exists(dest_path):
    os.mkdir(dest_path)


def main():
    saved_files_filename = 'saved_files.txt'
    if not os.path.isfile(saved_files_filename):
        open(saved_files_filename, 'w').close()
    with open(saved_files_filename) as f:
        saved_images = f.read().splitlines()
    source_images = os.listdir(source_path)
    new_images = filter_img_items(set(source_images) - set(saved_images))
    save_as_jpg(new_images)
    with open(saved_files_filename, 'a+') as f:
        f.write('\n'.join(new_images) + '\n')


def full_path(filename):
    return os.path.join(source_path, filename)


def filter_img_items(items):
    def is_fullhd(filename):
        with Image.open(full_path(filename)) as img:
            return (1920, 1080) == img.size

    return [i for i in items if is_fullhd(i)]


def save_as_jpg(items):
    saved_count = len(items)
    for i in items:
        try:
            copyfile(full_path(i), os.path.join(dest_path, str(time())) + '.jpg')
        except OSError:
            saved_count -= 1
    print(f'{saved_count} images has been saved to {dest_path}')


if __name__ == "__main__":
    main()
