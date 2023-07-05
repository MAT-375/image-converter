import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def processImage(filename, operation):
    print(f"the operation is {operation} and the file name is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            newFileName = f"static/{filename}"
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite( newFileName, imgProcessed )
            return newFileName
        case "cjpg":
            newFileName = f"static/{filename.rsplit('.', 1)[0]}.jpg"
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cwebp":
            newFileName = f"static/{filename.rsplit('.', 1)[0]}.webp"
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cpng":
            newFileName = f"static/{filename.rsplit('.', 1)[0]}.png"
            cv2.imwrite(newFileName , img)
            return newFileName

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/how-to-use")
def how():
    return render_template("how_to_use.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="POST":
        operation = request.form.get("operation")
        # return "POST request is here"
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error, no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation )
            flash(f"Your image has been processed and is available <a target='_blank' href='/{new}'>here</a>")
            return render_template("index.html")
    return render_template("index.html")


app.run(debug=True, port=5001)