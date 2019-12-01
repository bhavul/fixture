from flask import Flask
from flask import request, Response, jsonify
import image_util
from datetime import datetime
from flask import render_template
import os
import logging

image_util.create_output_data_dir_if_not_exists()
app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)

class APIResponse:
    def respond(self, error, result=None):
        status_code = '400' if error else '201'
        if error:
            result = {'status': 'Error', 'message':str(error)}
        return jsonify(result), status_code

@app.route('/')
def render_static():
    return render_template('index.html')

@app.route('/debug')
def debug():
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

@app.route('/image', methods=['POST'])
def save_labelled_image():
    """Create a labelled image in data directory."""
    
    response_obj = APIResponse()
    try:
        image_base64_string = request.json['base64']
        label = request.json['label']
        extension = request.json['extension']
        navigator_details = request.json['details']
        date = get_today_date_in_str()

        img_data = image_util.get_image_from_base64(image_base64_string)
        output_file_name = '{}_{}.{}'.format(date, label, extension)
        output_file_path = os.path.join(image_util.get_correct_output_dir(label), output_file_name)
        output_file_details_path = os.path.join("Details", output_file_name)
        image_util.save_image(output_file_path, img_data)
        image_util.save_image(output_file_details_path,
                navigator_details.encode())
        api_response_data = {'status': 'Success', 'message': 'File created at {}'.format(output_file_path)}
        app.logger.info(api_response_data)
        return response_obj.respond(error=None, result=api_response_data)
    except Exception as e:
        app.logger.info("ERROR",navigator_details,':', e)
        return response_obj.respond(e)


def get_today_date_in_str():
    now = datetime.now()
    return '{}_{}_{}'.format(now.year, now.month, now.month)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
