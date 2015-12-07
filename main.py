"""`main` is the top level module for your Flask application."""
import json
import logging
import uuid

from google.appengine.ext import ndb
from auth.token import AccessToken
from oauth2client import client
from automation import lighting
from status.people import PersonStatus

# Import the Flask Framework
from flask import Flask, redirect, request

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# TODO: Add authentication to all of these endpoints

@app.route('/sunrise', methods=['POST'])
def handle_sunrise():
    if not check_token():
        return "Token invalid".format(), 400

    return lighting.handle_sunrise()

@app.route('/get_access_token', methods=['GET'])
def register_user():

    # TODO: Make this work someday
    # https://developers.google.com/admin-sdk/directory/v1/guides/authorizing
    # flow = client.flow_from_clientsecrets('secrets.json',
    #                                       scope='https://www.googleapis.com/auth/admin.directory.group.member.readonly',
    #                                       redirect_uri='http://localhost:8080/check_group')
    # return redirect(flow.step1_get_authorize_url())

    # This part would go in the callback

    authable_user = False

    # Check that the oauthed user is in the Google Group whise members are allowed to use this service.

    if authable_user:
        token = uuid.uuid4().hex
        a_token = AccessToken(key=ndb.Key(AccessToken, token))
        a_token.put()
        return token, 200

    return "Authentication Failed", 500

def check_token():

    logging.info("Request data: %s", request.data)

    token = json.loads(request.data).get('access_token') if request.data else None
    if not token:
        return False

    found_token = ndb.Key(AccessToken, token).get()
    if found_token and found_token.active:
        return True

    return False

@app.route('/people/add', methods=['POST'])
def add_person():
    if not check_token():
        return "Token invalid".format(), 400

    person = PersonStatus(key=ndb.Key(PersonStatus, 'brad'),
                          name='brad')
    person.put()

    return "Person Created Successfully", 200

@app.route('/people/<name>/home', methods=['POST'])
def person_arrived_home(name):
    if not check_token():
        return "Token invalid".format(), 400

    person = ndb.Key(PersonStatus, name).get()
    if not person:
        logging.error("Attempted to mark user as arrived home: %s", name)
        return "Error", 400

    person.at_home = True
    person.put()
    return "Person Updated Successfully", 200

@app.route('/people/<name>/away', methods=['POST'])
def person_left_home(name):
    if not check_token():
        return "Token invalid".format(), 400

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
