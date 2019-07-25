from flask import Flask, render_template, request, make_response, redirect, url_for, flash, send_file, abort
from werkzeug.utils import secure_filename
import mosaik
import os
import uuid
import PIL
import io


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

image_store = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global image_store
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(404)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('root'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()

        image = PIL.Image.open(file, 'r')
        image.thumbnail((500, 500), PIL.Image.ANTIALIAS)
        image_store = image.copy()
        #image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(filename, 200)

@app.route('/convert', methods=['GET'])
def convert():
    print('bla')
    global image_store
    print('bla')
    #file_name = request.args.get('file')
    grid = int(request.args.get('grid'))
    grid = tuple( grid * i for i in (4, 3))
    
    new_image = mosaik.convert(image_store)
    print('bla')
    b = io.BytesIO()
    new_image.save(b, "JPEG")
    print('bla')

    return send_file(
    b,
    mimetype='image/jpeg',
    as_attachment=True,
    attachment_filename='l.jpg')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
