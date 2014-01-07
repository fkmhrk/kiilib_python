import client
import kiiobject
import bucket

class KiiContext(object):
    def __init__(self, app_id, app_key, url):
        self.app_id = app_id
        self.app_key = app_key
        self.url = url
        self.factory = client.KiiClientFactory()
        self.access_token = None

    def newClient(self):
        return self.factory.newClient()

class CloudException(Exception):
    def __init__(self, code, body):
        self.code = code
        self.body = body

    def __repr__(self):
        return 'HTTP %d %s' % (self.code, self.body)
    __str__ = __repr__

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class KiiApp(object):
    """
    >>> # just a singleton check =)
    >>> KiiApp().__repr__() == KiiApp().__repr__()
    True
    """
    __metaclass__ = Singleton
    def getPath(self):
        return ""
    def __repr__(self):
        return "app-scope"
APP_SCOPE = KiiApp()

class KiiUser(object):
    """
    A user in Kii Cloud. This class is immutable.
    """
    def __init__(self, userID=None, **fields):
        self.id = userID
        self.data = {k:v for (k,v) in fields.iteritems()}

    def getPath(self):
        if self.id == None:
            raise Exception("tried to generate URL while id is None")
        return 'users/%s' % (self.id)

    def __getattr__(self, name):
        return self.data.get(name)

    def __repr__(self):
        return "KiiUser(id:%s, %s)" % (self.id, ', '.join(["%s:%s" % (k, v) for (k, v) in self.data.iteritems()]))

class KiiGroup(object):
    def __init__(self, id):
        self.id = id

    def getPath(self):
        return 'groups/%s' % (self.id)

class AppAPI(object):
    def __init__(self, context):
        self.context = context
        self.objectAPI = kiiobject.ObjectAPI(context)
        self.bucketAPI = bucket.BucketAPI(context)
    
    def _login(self, body):
        url = '%s/oauth2/token' % self.context.url
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, False)
        (code, body) = client.send(body)
        if code != 200:
            raise CloudException(code, body)
        self.context.access_token = body['access_token']
        id = body['id']
        return KiiUser(id)

    def login(self, userIdentifier, password):
        return self._login(
            body = {
                'username' : userIdentifier,
                'password' : password
                }
        )

    def loginAsAdmin(self, client_id, client_secret):
        return self._login(
            body = {
                'client_id' : client_id,
                'client_secret' : client_secret
                }
        )

    def signup(self, username, password, **extFields):
        url = '%s/apps/%s/users' % (self.context.url, self.context.app_id)
        body = {
            'password' : password
            }
        if extFields != None:
            for k, v in extFields.items():
                body[k] = v
        if username != None:
            body['loginName'] = username
        
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, False)
        (code, body) = client.send(body)
        if code != 201:
            raise CloudException(code, body)
        id = body['userID']
        return KiiUser(userID=id, loginName=username, **extFields)

def doctest():
    import doctest
    import json
    doctest.testmod()

