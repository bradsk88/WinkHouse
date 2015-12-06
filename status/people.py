import logging

from google.appengine.ext import ndb

class PersonStatus(ndb.Model):

    name = ndb.StringProperty(required=True)
    at_home = ndb.BooleanProperty(default=False)

def is_person_home(name):
    person = ndb.Key(PersonStatus, name).get()
    if not person:
        logging.error("Attempting to check status of non-existent user: %s", name)
        return False
    return person.at_home