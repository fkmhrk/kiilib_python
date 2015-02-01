import kii
import copy

class KiiUser(dict):
    """
    >>> import json
    >>> user = KiiUser("id", f1="value1", f2=2)
    >>> json.dumps(obj) == json.dumps(dict(f1="value1", f2=2))
    True
    """
    def __init__(self, id, **data):
        self.id = id
        self.update(data)

    def getPath(self):
        """
        >>> user = KiiUser("id", f1="value1", f2=2)
        >>> user.getPath()
        'users/id'
        """
        return 'users/%s' % (self.id)

    def __repr__(self):
        return "KiiUser(%s) %s" % (self.id, { k:v for (k,v) in self.iteritems() })

class UserAPI:
    def __init__(self, context):
        self.context = context
        
    def refresh(self, user):
        """
        retrieve the user from cloud, and update its contents. This method returns nothing.
        """
        (code, body) = self.context.newClient().get(
            url='%s/apps/%s/%s' % (self.context.url, self.context.app_id, user.getPath()),
            context=self.context)
        if code >= 300:
            raise kii.CloudException(code, body)
        user.update(body)        
