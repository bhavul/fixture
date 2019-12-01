from flask import Flask
from flask import request, Response, jsonify
import image_util
from datetime import datetime
from flask import render_template
import os
import logging
import logging.handlers as handlers
import time
from constants import Directories, Config


app = Flask(__name__)
dir_obj = Directories()       # just initialise it so it creates required directories

class APIResponse:
    def respond(self, error, result=None):
        status_code = '400' if error else '201'
        if error:
            result = {'status': 'Error', 'message':str(error)}
        return jsonify(result), status_code

@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/image', methods=['POST'])
def save_labelled_image():
    """Create a labelled image in data directory."""
    
    response_obj = APIResponse()
    try:
        # read data from request
        image_base64_string = request.json['base64']
        label = request.json['label']
        extension = request.json['extension']
        navigator_details = request.json['details']

        # convert to image
        img_data = image_util.get_image_from_base64(image_base64_string)

        # save the image file and details file
        output_file_detail_path, output_file_path = get_output_files_path(dir_obj, extension, label)
        image_util.save_image(output_file_path, img_data)
        print(navigator_details, file=open(output_file_detail_path, 'w'))

        # return response
        api_response_data = {'status': 'Success', 'message': 'File created at {}'.format(output_file_path)}
        app.logger.info(api_response_data)
        return response_obj.respond(error=None, result=api_response_data)
    except Exception as e:
        app.logger.error("ERROR : {}".format(str(e)))
        return response_obj.respond(error=e, result=None)


def get_output_files_path(dir_obj, extension, label):
    date = get_today_date_in_str()
    current_unix_time = str(int(time.time()))
    output_file_prefix = '{}_{}_{}'.format(date, label, current_unix_time)
    output_file_name = '{}.{}'.format(output_file_prefix, extension)
    output_file_detail_name = '{}.{}'.format(output_file_prefix, 'txt')
    output_dir = dir_obj.get_correct_output_dir(label)
    output_file_path = os.path.join(output_dir, output_file_name)
    output_file_detail_path = os.path.join(output_dir, output_file_detail_name)
    return output_file_detail_path, output_file_path


def get_today_date_in_str():
    now = datetime.now()
    return '{}_{}_{}'.format(now.year, now.month, now.month)

def config_logging():
    log_file_dir = Directories.LOGGING_DIR
    log_filename = os.path.join(log_file_dir, 'app.log')
    log_handler = handlers.TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=30)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(log_handler)
    app.logger.setLevel(Config.LOGGING_LEVEL)

if __name__ == '__main__':
    config_logging()
    app.logger.info("Initialising app")
    app.run(host='0.0.0.0', port=5000, debug=True)
