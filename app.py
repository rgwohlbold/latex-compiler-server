import shutil
import os
import random
import string
import tempfile
import subprocess
import glob
from flask import Flask, Response, request, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = {'zip'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/")
def hello_world():
    if 'file' not in request.files:
        return Response("no file part", status=400)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return Response("file is empty or now allowed", status=400)
    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    directory = tempfile.mkdtemp()
    shutil.unpack_archive(filename, directory)

    p = subprocess.Popen(["latexmk", "-pdf"], cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
    if p.wait() != 0:
        stdout = p.stdout.read()
        stderr = p.stderr.read()
        shutil.rmtree(directory)
        os.remove(filename)
        return Response(stdout + stderr, status=400)
    pdf_file = glob.glob(directory + "/*.pdf")[0]
    response =  send_file(pdf_file, as_attachment=True)
    shutil.rmtree(directory)
    os.remove(filename)
    return response
