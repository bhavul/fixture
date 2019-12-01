import os
import pathlib

class Config:
    LOGGING_LEVEL = 'DEBUG'

class Constant:
    GOOD_POSTURE_LABEL = 'Good'
    BAD_POSTURE_LABEL = 'Bad'

class Directories:

    PROJECT_DIR = os.path.dirname(__file__)
    OUTPUT_DIR = os.path.join(PROJECT_DIR, 'Data')

    GOOD_POSTURE_DIR = os.path.join(OUTPUT_DIR, Constant.GOOD_POSTURE_LABEL)
    BAD_POSTURE_DIR = os.path.join(OUTPUT_DIR, Constant.BAD_POSTURE_LABEL)

    LOGGING_DIR = os.path.join(PROJECT_DIR, 'Logs')

    def __init__(self):
        # creating necessary directories if they didn't exist
        pathlib.Path(Directories.GOOD_POSTURE_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(Directories.BAD_POSTURE_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(Directories.LOGGING_DIR).mkdir(parents=True, exist_ok=True)

    def get_correct_output_dir(self, label):
        if label == Constant.GOOD_POSTURE_LABEL:
            return Directories.GOOD_POSTURE_DIR
        elif label == Constant.BAD_POSTURE_LABEL:
            return Directories.BAD_POSTURE_DIR
        else:
            raise ValueError('Label is out of syllabus.')
