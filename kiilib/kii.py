import client
import kiiobject

class KiiContext(object):
    def __init__(self, app_id, app_key, url):
        self.app_id = app_id
        self.app_key = app_key
        self.url = url
        self.factory = client.KiiClientFactory()

    def newClient(self):
        return self.factory.newClient()

class CloudException(Exception):
    def __init__(self, code, body):
        self.code = code
        self.body = body

    def __str__(self):
        return 'HTTP %d %s' % (self.code, self.body)

class KiiUser(object):
    """
    A user in Kii Cloud. This class is immutable.
    """
    # 'value-only' fields
    FIELD_KEYS = ['loginName', 'displayName', 'emailAddress', 'phoneNumber', 'country', 'emailVerified', 'phoneNumberVerified']
    def __init__(self, id=None, **fields):
        self.id = id
        self.data = {k:v for (k,v) in fields.iteritems() if k in self.FIELD_KEYS}

    def getPath(self):
        if self.id == None:
            raise Exception("tried to generate URL while id is None")
        return 'users/%s' % (self.id)

    @property
    def loginName(self):
        return self.data['loginName']

    @property
    def displayName(self):
        return self.data['displayName']

    @property
    def emailAddress(self):
        return self.data['emailAddress']

    @property
    def phoneNumber(self):
        return self.data['phoneNumber']

    @property
    def country(self):
        return self.data['country']

    @property
    def emailVerified(self):
        return self.data['emailVerified']

    @property
    def phoneNumberVerified(self):
        return self.data['phoneNumberVerified']

    def __str__(self):
        return "KiiUser(id:%s, %s)" % (self.id, ', '.join(["%s:%s" % (k, v) for (k, v) in self.data.iteritems()]))

class KiiGroup(object):
    def __init__(self, id):
        self.id = id

    def getPath(self):
        return 'groups/%s' % (self.id)

class KiiBucket(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def getPath(self):
        return '%s/buckets/%s' % (self.owner.getPath(), self.name)
        
class KiiObject(object):
    def __init__(self, bucket, id, data):
        self.bucket = bucket
        self.id = id
        self.data = data

    def getPath(self):
        return '%s/objects/%s' % (self.bucket.getPath(), self.id)
        
class AppAPI(object):
    def __init__(self, context):
        self.context = context
        self.objectAPI = kiiobject.ObjectAPI(context)
    
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
        return KiiUser(id=id, loginName=username)
        
