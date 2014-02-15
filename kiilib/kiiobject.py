import kii
import copy

class KiiObject(dict):
    """
    >>> import json
    >>> from bucket import *
    >>> obj = KiiObject(KiiBucket(kii.APP_SCOPE, "mybucket"), "id", f1="value1", f2=2)
    >>> json.dumps(obj) == json.dumps(dict(f1="value1", f2=2))
    True
    """
    def __init__(self, bucket, id, **data):
        self.bucket = bucket
        self.id = id
        self.update(data)

    def getPath(self):
        """
        >>> from bucket import *
        >>> # app scope
        >>> obj = KiiObject(KiiBucket(kii.APP_SCOPE, "mybucket"), "id", f1="value1", f2=2)
        >>> obj.getPath()
        'buckets/mybucket/objects/id'
        >>> # group scope
        >>> obj = KiiObject(KiiBucket(kii.KiiGroup("mygroup"), "mybucket"), "id", f1="value1", f2=2)
        >>> obj.getPath()
        'groups/mygroup/buckets/mybucket/objects/id'
        >>> # user scope
        >>> obj = KiiObject(KiiBucket(kii.KiiUser("myuser"), "mybucket"), "id", f1="value1", f2=2)
        >>> obj.getPath()
        'users/myuser/buckets/mybucket/objects/id'
        """
        return '%s/objects/%s' % (self.bucket.getPath(), self.id)

    def __repr__(self):
        return "KiiObject(%s, %s) %s" % (self.bucket, self.id, { k:v for (k,v) in self.iteritems() })
        
class ObjectAPI:
    def __init__(self, context):
        self.context = context

    def create(self, bucket, **data):
        url = '%s/apps/%s/%s/objects' % (self.context.url,
                                      self.context.app_id,
                                      bucket.getPath())
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(data)
        if code != 201:
            raise kii.CloudException(code, body)
        id = body['objectID']
        created = body['createdAt']
        datatype = body['dataType']
        return KiiObject(bucket, id, _id=id, _modified=created, _created=created, _dataType=datatype, **data)
        
    def save(self, obj):
        """
        save the passed object and update the modification time. This meethod returns nothing.
        """
        url = '%s/apps/%s/%s' % (self.context.url, self.context.app_id, obj.getPath())
        client = self.context.newClient()
        client.method = "PUT"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(obj)
        if code >= 300:
            raise kii.CloudException(code, body)
        udpated = copy.copy(obj)
        obj['_modified'] = body['modifiedAt']

    def delete(self, obj):
        (code, body) = self.context.newClient().delete(
            url='%s/apps/%s/%s' % (self.context.url, self.context.app_id, obj.getPath()),
            context=self.context)
        if code >= 300:
            raise kii.CloudException(code, body)

    def refresh(self, obj):
        """
        retrieve the object from cloud, and update its contents. This method returns nothing.
        """
        (code, body) = self.context.newClient().get(
            url='%s/apps/%s/%s' % (self.context.url, self.context.app_id, obj.getPath()),
            context=self.context)
        if code >= 300:
            raise kii.CloudException(code, body)
        obj.update(body)

    def updateBody(self, obj, type, data, size):
        url = '%s/apps/%s%s/body' % (self.context.url,
                                      self.context.app_id,
                                      obj.getPath())
        client = self.context.newClient()
        client.method = "PUT"
        client.url = url
        client.setContentType(type)
        client.setKiiHeaders(self.context, True)
        (code, body) = client.sendFile(data, size)
        if code == 200:
            return
        if code == 201:
            return
        raise kii.CloudException(code, body)
 
    def downloadBody(self, obj, outFile):
        url = '%s/apps/%s%s/body' % (self.context.url,
                                      self.context.app_id,
                                      obj.getPath())
        client = self.context.newClient()
        client.method = "GET"
        client.url = url
        client.setKiiHeaders(self.context, True)
        (code, body) = client.sendForDownload(outFile)
        if code == 200:
            return
        raise kii.CloudException(code, body)

def doctest():
    import doctest
    import json
    doctest.testmod()


