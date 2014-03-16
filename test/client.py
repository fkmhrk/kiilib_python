import json
import mimetypes
import StringIO

class MockClientFactory:
    def __init__(self):
        self.client = MockClient()
        
    def newClient(self):
        return self.client

class MockResponse:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

class MockClient:
    def __init__(self):
        self.responses = []
        self.headers = {}
        self.content_type = None

    def setContentType(self, value):
        self.content_type = value
        
    def setKiiHeaders(self, context, auth_required):
        self.headers['x-kii-appid'] = context.app_id
        self.headers['x-kii-appkey'] = context.app_key
        if auth_required and context.access_token != None:
            self.headers['authorization'] = 'Bearer %s' % context.access_token

    def get(self, url, context, authRequired=True):
        response = self.responses.pop(0)
        #self.url = url
        #self.setKiiHeaders(context, authRequired)
        #self.method = "GET"
        return (response.status, json.loads(response.body))

    def delete(self, url, context, authRequired=True):
        self.url = url
        self.setKiiHeaders(context, authRequired)
        self.method = "DELETE"
        return self._sendOnly()
        
    def send(self, data = None):
        (code, body) = self._sendOnly(data)
        return (code, json.loads(body))

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
