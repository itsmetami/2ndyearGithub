
from flask import Flask, flash, request, redirect, url_for, render_template, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)  # gina kwa ya tanan nga elements ka folder


    return render_template('photo_Uplaod.html', filename = files)

@app.route('/', methods=['POST'])
def upload_image():


    file = request.files['file']


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        # secure_filename is a function provided by Flask's werkzeug.utils module that is used to sanitize and secure filenames before storing them on the server. This is important for security reasons.
        # When users upload files, the filenames may contain special characters, spaces, or other potentially harmful elements. By using secure_filename, you ensure that the filename is transformed into a safer version. It removes or replaces characters that could be used for malicious purposes, such as directory traversal attacks.

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        files = os.listdir(UPLOAD_FOLDER) # gina kwa ya tanan nga elements ka folder

        print(files)
        flash('Image successfully uploaded and displayed below')

        return render_template('photo_Uplaod.html',filename =files)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')



@app.route("/delpic", methods=['post'])
def delpic():


    picture_del = request.form['todel']
    print(picture_del)

    os.remove(f'static/uploads/{picture_del}')

    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)

