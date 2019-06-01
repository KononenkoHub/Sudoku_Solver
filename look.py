import os
import time
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ROOT = os.path.dirname(__file__)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/cache/')
    print(target)

    if not os.path.isdir(target):
        os.makedirs(target)
    for the_file in os.listdir(target):
        file_path = os.path.join(target, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = '/'.join([target, filename])
        newdestination = '/'.join([target, 'sudoku.jpg'])
        print(destination)
        file.save(destination)
        os.renames(destination, newdestination)
        os.system('python solution.py')
    return render_template('load.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)