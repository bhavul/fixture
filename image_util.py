import base64
import pathlib
from constants import Constant
from constants import Directories

def get_image_from_base64(base64string):
    return base64.b64decode(base64string)

def save_image(file_path, image_data):
    with open(file_path, 'wb') as f:
        f.write(image_data)

def create_output_data_dir_if_not_exists():
    pathlib.Path(Directories.GOOD_POSTURE_DIR).mkdir(parents=True, exist_ok=True)
    pathlib.Path(Directories.BAD_POSTURE_DIR).mkdir(parents=True, exist_ok=True)

def get_correct_output_dir(label):
    if label == Constant.GOOD_POSTURE_LABEL:
        return Directories.GOOD_POSTURE_DIR
    elif label == Constant.BAD_POSTURE_LABEL:
        return Directories.BAD_POSTURE_DIR
    else:
        raise ValueError('Label is out of syllabus.')