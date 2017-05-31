import getpass
import os
import sys
from PIL import Image
from shutil import copyfile
from time import time

source_path = os.path.join(os.getenv('LOCALAPPDATA'),
                           r'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')
min_size = 200_000

dest_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spotlight')
if not os.path.exists(dest_path):
    os.mkdir(dest_path)


def main():
    saved_files_filename = 'saved_files.txt'
    if not os.path.isfile(saved_files_filename):
        open(saved_files_filename, 'w').close()
    with open(saved_files_filename) as f:
        saved_imgs = f.read().splitlines()
    all_imgs = os.listdir(source_path)
    new_imgs = filter_img_items(set(all_imgs) - set(saved_imgs))
    save_as_jpg(new_imgs)
    with open(saved_files_filename, 'a+') as f:
        f.write('\n'.join(new_imgs) + '\n')


def full_path(filename):
    return os.path.join(source_path, filename)


def filter_img_items(items):
    def is_fullhd(filename):
        with Image.open(full_path(filename)) as img:
            w, h = img.size
        return w == 1920 and h == 1080

    return [i for i in items if os.stat(os.path.join(source_path, i)).st_size >= min_size and is_fullhd(i)]


def save_as_jpg(items):
    saved_count = len(items)
    for i in items:
        try:
            copyfile(full_path(i), os.path.join(dest_path, str(time())) + '.jpg')
        except OSError:
            saved_count -= 1
    print('{} images has been saved to {}'.format(saved_count, dest_path))


if __name__ == "__main__":
    main()
