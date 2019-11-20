from flask import Flask
from flask import render_template, url_for, redirect, session, flash, request
import os
from flask import send_file, send_from_directory, safe_join, abort
import hashlib
import base64
from PIL import Image
import io
from werkzeug.utils import secure_filename
import requests 
import json
import uuid
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.datastructures import FileStorage
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


#TOP_LEVEL_DIR = 

# Uploads
UPLOADS_DEFAULT_DEST = '/project/static/pdf/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/pdf/'
 
UPLOADED_IMAGES_DEST = '/project/static/img/'
UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'

app = Flask(__name__, instance_relative_config=True)

app.config['UPLOADED_DEFAULT_DEST'] = '/var/uploads'
# Configure the image uploading via Flask-Uploads
#images = UploadSet('images', IMAGES)
pdf = UploadSet(extensions=('pdf','txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml'), default_dest=lambda app: app.instance_path)
configure_uploads(app, pdf)
#configure_uploads(app, (images), lambda app: '/var/uploads')

photos = UploadSet('photos', IMAGES, default_dest=lambda app: app.instance_path)
configure_uploads(app, photos)


images = UploadSet(extensions=('pdf','txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml'), default_dest=lambda app: app.instance_path)
configure_uploads(app, images)


#UPLOAD_FOLDER = '/home/sevenbits/Desktop/PDF-EDITOR-QR-ATTACH/project/tmp'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#MYDIR = os.path.dirname(lambda app: app.instance_root)






#media = UploadSet('media', default_dest=lambda app: app.instance_root)

# class UploadForm(FlaskForm):
#     pdffile = FileField(validators=[FileAllowed(pdf, u'pdf only!'), FileRequired(u'File was empty!')]) 
#     photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
#     submit = SubmitField(u'Upload')


@app.route('/')
def home():
    path = generateqr()
    return render_template('home.html',path=path, name="home")

@app.route('/generateqr')
def generateqr():
    user= "shah.yogi+3@tristonsoft.com"
    key1 = "5f24f8087b6228edf456bb0da030c67c127a2fec"
    secret_key1= "KoGLt29m51dI8jeVz7rvzljUdGNMf9IdeEZP13M8KhChgjkCd4Z9EghLa9We"
    secret=key1+secret_key1
    hash_object = hashlib.sha256(str(secret).encode('utf-8'))
    payload = hash_object.hexdigest()
    url='http://veridocglobaldeveloper-stage.azurewebsites.net/api/generateqr'
    headers={'apikey':key1,'payload':payload,'content_type':'application/json'}
    header = {'content_type': 'application/json'}
    r=requests.post(url,headers=headers)
    data=r.json()
    a=json.dumps(data['uniqueId']).strip('"')
    b=json.dumps(data['qrImage'])
    arr = []
    arr = b.split(',')
    b1 = arr[1]
    image = base64.b64decode(str(b1))
    file_name = uuid.uuid4().hex[:50].upper()
    fileExtension = '.png'
    file_name += fileExtension
    image_path = file_name
    im = Image.open(io.BytesIO(image))
    newsize = (200, 200) 
    im1 = im.resize(newsize)
    im1.save(image_path)
    #images.save(im1)
    return image_path

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        filename = pdf.save(request.files['file'])
        #print(request.files['file'])
        url1 = pdf.url(filename)
        #print(url1)
        #filename2 = pdf.save(request.files['image'],'htmlfi')  
        url2=""
        #print(url2)
        #url2 = ""
        return render_template("index.html",qrimg=url2,file_path=url1)

# @app.route('/uploads/')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST' and 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         rec = Photo(filename=filename, user=g.user.id)
#         rec.store()
#         flash("Photo saved.")
#         return redirect(url_for('show', id=rec.id))
#     return render_template('upload.html')

# @app.route('/photo/<id>')
# def show(id):
#     photo = Photo.load(id)
#     if photo is None:
#         abort(404)
#     url = photos.url(photo.filename)
#     return render_template('show.html', url=url, photo=photo)


if __name__ == '__main__':
    app.run(debug=True)