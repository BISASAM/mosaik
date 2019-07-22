from flask import Flask, render_template, request, make_response, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
import mosaik
import os
import uuid


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        abort(404)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('root'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(filename, 200)

@app.route('/convert', methods=['GET'])
def convert():
    file_name = request.args.get('file')
    new_image_path = mosaik.convert(os.path.join(app.config['UPLOAD_FOLDER'], file_name), grid_size=(4, 3))
    return make_response(new_image_path, 200)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('converted', 'result.jpg' )


if __name__ == '__main__':
    app.run(port=3000, debug=True)
