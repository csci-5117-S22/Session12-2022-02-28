from flask import Flask, render_template, request, g, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import io

import db

app = Flask(__name__)

# have the DB submodule set itself up before we get started. groovy.
@app.before_first_request
def initialize():
    db.setup()

@app.route('/')
def home():
    
    return render_template('main.html', top_gift = db.get_most_popular_gift())

@app.route('/people', methods=['GET'])
def people():
    return render_template("people.html", people=db.get_people())

@app.route('/people', methods=['POST'])
def new_person():
    name = request.form.get("name", "unnamed friend")
    db.add_person(name)
    return redirect(url_for('people'))

@app.route('/people/<person_id>', methods=['GET'])
def get_person(person_id):
    name = db.get_name_for_person(person_id)
    gifts = db.get_gifts_for_person(person_id)
    return render_template("person.html", name=name, gifts=gifts)

@app.route('/api/foo')
def api_foo():
    data = {
        "message": "hello, world",
        "isAGoodExample": False,
        "aList": [1, 2, 3],
        "nested": {
            "key": "value"
        }
    }
    return jsonify(data)



### IMAGES
@app.route('/image/<int:img_id>')
def view_image(img_id):
    image_row = db.get_image(img_id)
    stream = io.BytesIO(image_row["data"])
         
    # use special "send_file" function
    return send_file(stream, attachment_filename=image_row["filename"])    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', "gif"]


@app.route('/image', methods=['POST'])
def upload_image():
    # check if the post request has the file part
    if 'image' not in request.files:
        return redirect(url_for("image_gallery", status="Image Upload Failed: No selected file"))
    file = request.files['image']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(url_for("image_gallery", status="Image Upload Failed: No selected file"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        data = file.read()
        db.upload_image(data, filename)
        
    return redirect(url_for("image_gallery", status="Image Uploaded Succesfully"))
        
@app.route('/image', methods=['GET'])
def image_gallery():
    status = request.args.get("status", "")
    
    with db.get_db_cursor() as cur:
        image_ids = db.get_image_ids()
        return render_template("gallery.html", image_ids = image_ids)



