"""`main` is the top level module for your Flask application."""
import logging
from google.appengine.ext import ndb
from oauth2client import client
from automation import lighting
from status.people import PersonStatus

# Import the Flask Framework
from flask import Flask, redirect
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# TODO: Add authentication to all of these endpoints

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello Bitch!'

@app.route('/sunrise')
def handle_sunrise():
    return lighting.handle_sunrise()

@app.route('/register')
def register_user():
    # https://developers.google.com/admin-sdk/directory/v1/guides/authorizing
    flow = client.flow_from_clientsecrets('secrets.json',
                                          scope='https://www.googleapis.com/auth/admin.directory.group.member.readonly',
                                          redirect_uri='http://localhost:8080/check_group')
    return redirect(flow.step1_get_authorize_url())

@app.route('/check_group')
def check_group():
    oauth_code = request.args.get('code')
    return "Oauth done", 200

@app.route('/people/add')
def add_person():
    person = PersonStatus(key=ndb.Key(PersonStatus, 'brad'), name='brad')
    person.put()
    return "Person Created Successfully", 200

@app.route('/people/<name>/home')
def person_arrived_home(name):
    person = ndb.Key(PersonStatus, name).get()
    if not person:
        logging.error("Attempted to mark user as arrived home: %s", name)
        return "Error", 400

    person.at_home = True
    person.put()
    return "Person Updated Successfully", 200

@app.route('/people/<name>/away')
def person_left_home(name):
    person = ndb.Key(PersonStatus, name).get()
    if not person:
        logging.error("Attempted to mark user as left home: %s", name)
        return "Error", 400

    person.at_home = False
    person.put()
    return "Person Updated Successfully", 200

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error', 500
