import os
import pathlib

class Constant:
    GOOD_POSTURE_LABEL = 'Good'
    BAD_POSTURE_LABEL = 'Bad'

class Directories:

    PROJECT_DIR = os.path.dirname(__file__)
    OUTPUT_DIR = os.path.join(PROJECT_DIR, 'Data')

    GOOD_POSTURE_DIR = os.path.join(OUTPUT_DIR, Constant.GOOD_POSTURE_LABEL)
    BAD_POSTURE_DIR = os.path.join(OUTPUT_DIR, Constant.BAD_POSTURE_LABEL)