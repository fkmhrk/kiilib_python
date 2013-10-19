import client
import object

class KiiContext:
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

class KiiUser:
    def __init__(self, id):
        self.id = id

    def getPath(self):
        return 'users/%s' % (self.id)

class KiiGroup:
    def __init__(self, id):
        self.id = id

    def getPath(self):
        return 'groups/%s' % (self.id)

class KiiBucket:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def getPath(self):
        return '%s/buckets/%s' % (self.owner.getPath(), self.name)
        
class KiiObject:
    def __init__(self, bucket, id, data):
        self.bucket = bucket
        self.id = id
        self.data = data

    def getPath(self):
        return '%s/objects/%s' % (self.bucket.getPath(), self.id)
        
class AppAPI:
    def __init__(self, context):
        self.context = context
        self.objectAPI = object.ObjectAPI(context)
    
    def login(self, userIdentifier, password):
        url = '%s/oauth2/token' % self.context.url
        body = {
            'username' : userIdentifier,
            'password' : password
            }
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
        print KiiUser(id)

    def signup(self, userIdentifier, password):
        url = '%s/apps/%s/users' % (self.context.url, self.context.app_id)
        body = {
            'loginName' : userIdentifier,
            'password' : password
            }
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, False)
        (code, body) = client.send(body)
        if code != 201:
            raise CloudException(code, body)
        id = body['id']
        print user.KiiUser(id)        
        
