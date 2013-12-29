import urllib2
import json
import mimetypes
import StringIO

class KiiClientFactory:
    def newClient(self):
        return KiiClient()

class KiiClient:
    def __init__(self):
        self.headers = {}

    def setContentType(self, value):
        self.content_type = value
        
    def setKiiHeaders(self, context, auth_required):
        self.headers['x-kii-appid'] = context.app_id
        self.headers['x-kii-appkey'] = context.app_key
        if auth_required:
            self.headers['authorization'] = 'Bearer %s' % context.access_token
        
    def send(self, data = None):
        req = urllib2.Request(
            url = self.url,
            headers = self.headers)
        req.get_method = lambda : self.method
        if data != None:
            data = json.dumps(data, sort_keys=True, ensure_ascii=False)
            data = data.encode('UTF-8')
            req.add_header('content-length', '%d' % len(data))
            req.add_data(StringIO.StringIO(data))
            req.add_header('content-type', self.content_type)

        try:
            resp = urllib2.urlopen(req)
            body = json.loads(resp.read())
            return (resp.code, body)
        except urllib2.HTTPError, e:
            body = json.loads(e.read())
            return (e.code, body)

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
