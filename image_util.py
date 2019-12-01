import base64
import pathlib
from constants import Constant
from constants import Directories

def get_image_from_base64(base64string):
    return base64.b64decode(base64string)

def save_image(file_path, image_data):
    with open(file_path, 'wb') as f:
        f.write(image_data)

