from flask import Flask, render_template, request, g, redirect, url_for, jsonify

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
