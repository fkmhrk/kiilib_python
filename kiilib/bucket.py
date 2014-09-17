import kii
import kiiobject
import collections

class BucketAPI(object):
    def __init__(self, context):
        self.context = context

    def query(self, bucket, condition):
        client = self.context.newClient()
        client.method = "POST"
        client.url = "%s/apps/%s/%s/%s" % (self.context.url, self.context.app_id, bucket.getPath(), "query")
        client.setContentType('application/vnd.kii.QueryRequest+json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(condition)
        if code != 200:
            raise kii.CloudException(code, body)
        nextKey = body.get("nextPaginationKey")
        condition.setPaginationKey(nextKey)
        return [kiiobject.KiiObject(bucket, o["_id"], **o) for o in body["results"]]

class KiiBucket(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def getPath(self):
        # :(
        if self.owner == kii.APP_SCOPE:
            return "buckets/%s" % self.name
        return '%s/buckets/%s' % (self.owner.getPath(), self.name)

    def __repr__(self):
        return "KiiBucket(%s, %s) " % (self.owner, self.name)


class KiiCondition(collections.defaultdict):
    """
    >>> import json
    >>> a = KiiCondition(KiiClause.equals('a', 10))
    >>> json.dumps(a, sort_keys=True) == json.dumps({'bucketQuery':{'clause':{'type':'eq', 'field':'a', 'value':10}}}, sort_keys=True)
    True
    """
    def __init__(self, clause, orderBy = None, decending=None, limit=None, paginationKey=None):
        bucketQuery = {}
        bucketQuery["clause"] = clause
        if orderBy != None : bucketQuery["orderBy"] = orderBy
        if decending != None : bucketQuery["decending"] = decending
        if limit != None : self["bestEffortLimit"] = limit
        if paginationKey != None : self["paginationKey"] = paginationKey
        self['bucketQuery'] = bucketQuery
    def setPaginationKey(self, key):
        self['paginationKey'] = key

    def hasNext(self):
        return self['paginationKey'] != None
    

class KiiClause(collections.defaultdict):
    def __init__(self, type, **data):
        self["type"]= type
        self.update(data)

    @staticmethod
    def all():
        """
        >>> import json
        >>> a = KiiClause.all()
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'all'}, sort_keys=True)
        True
        """
        return KiiClause('all')

    @staticmethod
    def equals(field, value):
        """
        >>> import json
        >>> a = KiiClause.equals("N", "V")
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'eq', 'field': 'N', 'value': 'V'}, sort_keys=True)
        True
        >>> a = KiiClause.equals("N", 123)
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'eq', 'field': 'N', 'value': 123}, sort_keys=True)
        True
        """
        return KiiClause('eq', field=field, value=value)

    @staticmethod
    def greaterThan(field, value, included):
        """
        >>> import json
        >>> a = KiiClause.greaterThan("f", 100, True)
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'range', 'field': 'f', 'lowerLimit': 100, 'lowerIncluded': True}, sort_keys=True)
        True
        """
        return KiiClause('range', field=field, lowerLimit=value, lowerIncluded=included)

    @staticmethod
    def lessThan(field, value, included):
        """
        >>> import json
        >>> a = KiiClause.lessThan("f", 200, False)
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'range', 'field': 'f', 'upperLimit': 200, 'upperIncluded': False}, sort_keys=True)
        True
        """
        return KiiClause('range', field=field, upperLimit=value, upperIncluded=included)

    @staticmethod
    def range(field, lowerValue, lowerIncluded, upperValue, upperIncluded):
        """
        >>> import json
        >>> a = KiiClause.range("f", 200, False, 500, True)
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'range', 'field': 'f', 'lowerLimit': 200, 'lowerIncluded':False, 'upperLimit': 500, 'upperIncluded': True}, sort_keys=True)
        True
        """
        return KiiClause('range', field=field, lowerLimit=lowerValue, lowerIncluded=lowerIncluded, upperLimit=upperValue, upperIncluded=upperIncluded)

    @staticmethod
    def inClause(field, values):
        """
        >>> import json
        >>> a = KiiClause.inClause("f", [1,2,3,5,8,13])
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'in', 'field': 'f', 'values': [1,2,3,5,8,13]}, sort_keys=True)
        True
        """
        return KiiClause("in", field=field, values=values)

    @staticmethod
    def notClause(clause):
        """
        >>> import json
        >>> a = KiiClause.notClause(KiiClause.equals("a", 100))
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'not', 'clause': {'type': 'eq', 'field': 'a', 'value': 100}}, sort_keys=True)
        True
        """
        return KiiClause('not', clause=clause)

    @staticmethod
    def andClause(clauses):
        """
        >>> import json
        >>> a = KiiClause.andClause([KiiClause.equals("a", 100), KiiClause.equals("b", 200)])
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'and', 'clauses': [{'type': 'eq', 'field': 'a', 'value': 100}, {'type':'eq', 'field':'b', 'value':200}]}, sort_keys=True)
        True
        """
        return KiiClause('and', clauses=clauses)

    @staticmethod
    def orClause(clauses):
        """
        >>> import json
        >>> a = KiiClause.orClause([KiiClause.equals("a", 100), KiiClause.equals("b", 200)])
        >>> json.dumps(a, sort_keys=True) == json.dumps({'type': 'or', 'clauses': [{'type': 'eq', 'field': 'a', 'value': 100}, {'type':'eq', 'field':'b', 'value':200}]}, sort_keys=True)
        True
        """
        return KiiClause('or', clauses=clauses)

def doctest():
    import doctest
    import json
    doctest.testmod()

if __name__ == "__main__":
    doctest()
