from google.appengine.ext import ndb


class AccessToken(ndb.Model):

    token = ndb.ComputedProperty(lambda self: self.key.id())
    active = ndb.BooleanProperty(default=True)
