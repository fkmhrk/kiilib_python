import json
import mimetypes
import StringIO

class MockClientFactory(object):
    def __init__(self):
        self.client = MockClient()
        
    def newClient(self):
        return self.client

class MockRequest(object):
    def __init__(self):
        self.content_type = None
        
class MockResponse(object):
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

class MockClient(object):
    def __init__(self):
        self.request = MockRequest()
        self.requests = []
        self.responses = []
        self.headers = {}
        self.content_type = None

    def setContentType(self, value):
        self.request.content_type = value
        
    def setKiiHeaders(self, context, auth_required):
        self.headers['x-kii-appid'] = context.app_id
        self.headers['x-kii-appkey'] = context.app_key
        if auth_required and context.access_token != None:
            self.headers['authorization'] = 'Bearer %s' % context.access_token

    def get(self, url, context, authRequired=True):
        self.request.method = "GET"
        self.request.url = url
        self.requests.append(self.request)
        self.request = MockRequest()
        
        response = self.responses.pop(0)
        return (response.status, json.loads(response.body))

    def delete(self, url, context, authRequired=True):
        self.request.method = "DELETE"
        self.request.url = url
        self.requests.append(self.request)
        self.request = MockRequest()
        
        response = self.responses.pop(0)
        if response.body == '':
            return (response.status, {})
        return (response.status, json.loads(response.body))
        
    def send(self, data = None):
        self.request.url = self.url
        self.request.method = self.method
        self.requests.append(self.request)
        self.request = MockRequest()
        
        response = self.responses.pop(0)
        return (response.status, json.loads(response.body))

    def _sendOnly(self, data = None):
        req = urllib2.Request(
            url = self.url,
            headers = self.headers)
        req.get_method = lambda : self.method
        if data != None:
            data = json.dumps(data, sort_keys=True, ensure_ascii=False)
            data = data.encode('UTF-8')
            req.add_header('content-length', '%d' % len(data))
            req.add_data(StringIO.StringIO(data))
            if self.content_type != None:
                req.add_header('content-type', self.content_type)

        try:
            resp = urllib2.urlopen(req)
            return (resp.code, resp.read())
        except urllib2.HTTPError, e:
            return (e.code, e.read())

    def sendFile(self, data, size):
        req = urllib2.Request(
            url = self.url,
            headers = self.headers)
        req.get_method = lambda : self.method
        req.add_data(data)
        req.add_header('content-type', self.content_type)
        req.add_header('content-length', '%d' % size)

        try:
            resp = urllib2.urlopen(req)
            body = json.loads(resp.read())
            return (resp.code, body)
        except urllib2.HTTPError, e:
            body = json.loads(e.read())
            return (e.code, body)            

    def sendForDownload(self, outFile):
        req = urllib2.Request(
            url = self.url,
            headers = self.headers)
        req.get_method = lambda : self.method
        try:
            resp = urllib2.urlopen(req)
            outFile.write(resp.read())
            return (resp.code, '')
        except urllib2.HTTPError, e:
            body = json.loads(e.read())
            return (e.code, body)        
