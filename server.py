from flask import Flask, render_template, request, g, redirect, url_for, jsonify, send_file, session, abort
from werkzeug.utils import secure_filename
import io

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from html_sanitizer import Sanitizer
sanitizer = Sanitizer()  # default configuration

import db

app = Flask(__name__)
app.secret_key = env["flask_session_secret"]

oauth = OAuth(app)

AUTHO0_CLIENT_ID = env['auth0_client_id']
AUTHO0_CLIENT_SECRET = env['auth0_client_secret']
AUTHO0_DOMAIN = env['auth0_domain']

auth0 = oauth.register(
    'auth0',
    client_id=AUTHO0_CLIENT_ID,
    client_secret=AUTHO0_CLIENT_SECRET,
    api_base_url='https://'+AUTHO0_DOMAIN,
    access_token_url='https://'+AUTHO0_DOMAIN+'/oauth/token',
    authorize_url='https://'+AUTHO0_DOMAIN+'/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# have the DB submodule set itself up before we get started. groovy.
@app.before_first_request
def initialize():
    db.setup()



###### AUTH STUFF

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    db.create_or_update_user(userinfo['sub'], userinfo['name'], userinfo['picture'])

    return redirect(url_for('get_person', person_id = userinfo['sub']))

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback_handling', _external = True))

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTHO0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/')
def home():
    return render_template('main.html', people=db.get_people())

@app.route('/people/<person_id>', methods=['GET'])
def get_person(person_id):
    profile = db.get_person(person_id)
    gifts = db.get_gifts_for_person(person_id)
    return render_template("person.html", profile=profile, gifts=gifts)

@app.route('/people/<person_id>', methods=['POST'])
def save_person(person_id):
    description = request.form['quill-html']
    # let's not allow stored XSS attacks shall we?
    description = sanitizer.sanitize(description)

    db.update_description(person_id, description)

    profile = db.get_person(person_id)
    gifts = db.get_gifts_for_person(person_id)
    return render_template("person.html", profile=profile, gifts=gifts)

@app.route('/people/<person_id>/gift', methods=['POST'])
def add_gift(person_id):
    # CUSTOM AUTH -- only if logged in, and not an idea for yourself..
    if 'profile' in session and session['profile']['user_id'] != person_id:
        name = request.form['idea']
        link = request.form['link']
        
        db.add_idea(person_id, name, link)

    return redirect(url_for('get_person', person_id = person_id))

@app.route('/gift/<gift_id>', methods=['POST'])
def buy_gift(gift_id):
    # in theory we should do some more custom auth here. that's on the TODO list.
    if 'profile' in session:
        bought = request.form['bought']
        db.update_gift(gift_id, bought)
        return jsonify(status="OK")
    else:
        return jsonify(status="error", message="you have to be logged in."), 403
