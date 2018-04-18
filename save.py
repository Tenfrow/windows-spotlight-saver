import os
import sys
from PIL import Image
from shutil import copyfile
from time import time

SOURCE_PATH = os.path.join(os.getenv('LOCALAPPDATA'),
                           r'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')

DEST_PATH = sys.argv[1] if (len(sys.argv) > 1) else os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                 'spotlight')

if not os.path.exists(DEST_PATH):
    os.mkdir(DEST_PATH)


def main():
    saved_count = 0
    for filename in os.listdir(SOURCE_PATH):
        file_path = os.path.join(SOURCE_PATH, filename)
        try:
            if is_fullhd(file_path) and is_unique(file_path):
                save_as_jpg(file_path, DEST_PATH)
                saved_count += 1
        except Exception as e:
            print(e)
    print(f'{saved_count} new images have been saved to {DEST_PATH}')
    input("Press Enter to exit")


def save_as_jpg(file_path, destination):
    """
    :param file_path: full path of the file to be saved
    :param destination: destination folder
    """
    copyfile(file_path, os.path.join(destination, str(time())) + '.jpg')


def is_fullhd(filename):
    """
    Returns True if the image is 1920 by 1080 pixels
    :param filename: full path of the file to be checked
    :rtype: bool
    """
    with Image.open(filename) as img:
        return img.size == (1920, 1080)


saved_files = set()


def is_unique(filename):
    """
    This check uses only comparison by size of images so it is not perfect,
    but for this task it should be enough to guarantee uniqueness.
    :param filename: Full path of the file to be checked
    :rtype: bool
    """
    global saved_files

    if not saved_files:
        saved_files = set(map(lambda fname: os.stat(os.path.join(DEST_PATH, fname)).st_size, os.listdir(DEST_PATH)))

    if os.stat(filename).st_size in saved_files:
        return False
    return True


if __name__ == "__main__":
    main()
