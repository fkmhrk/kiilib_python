import kii
import kiiobject

class BucketAPI(object):
    def __init__(self, context):
        self.context = context

    def query(self, bucket, condition):
        client = self.context.newClient()
        client.method = "POST"
        client.url = "%s/apps/%s/%s/%s" % (self.context.url, self.context.app_id, bucket.getPath(), "query")
        print client.url
        client.setContentType('application/vnd.kii.QueryRequest+json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(condition.toDict())
        print body
        if code != 200:
            raise kii.CloudException(code, body)
        return [kiiobject.KiiObject(bucket, o["_id"], o) for o in body["results"]]

class KiiBucket(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def getPath(self):
        return '%s/buckets/%s' % (self.owner.getPath(), self.name)


class KiiCondition(object):
    def __init__(self, clause, orderBy = None, decending=None, limit=None, pagenationKey=None):
        self.clause = clause
        self.orderBy = orderBy
        self.decending = decending
        self.limit = limit
        self.pagenationKey = pagenationKey

    def toDict(self):
        # pick up all non-None fields
        query = {k:self.__dict__[k] for k in ("orderBy", "decending", "limit", "pagenationKey") if self.__dict__[k] != None}
        query["clause"] = self.clause.toDict()
        return {"bucketQuery":query}


class KiiClause(object):
    def __init__(self, type, **data):
        self.type = type
        self.data = data

    def toDict(self):
        result = {"type": self.type}
        result.update({k:self.toDictAll(v) for (k,v) in self.data.iteritems()})
        return result

    def toDictAll(self, v):
        if isinstance(v, KiiClause):
            return v.toDict()
        elif isinstance(v, list) or isinstance(v, tuple):
            if len(v) > 0 and isinstance(v[0], KiiClause):
                return [x.toDict() for x in v]
        return v

    @staticmethod
    def all():
        """
        >>> a = KiiClause.all()
        >>> a.toDict() == {'type': 'all'}
        True
        """
        return KiiClause('all')

    @staticmethod
    def equals(field, value):
        """
        >>> a = KiiClause.equals("N", "V")
        >>> a.toDict() == {'type': 'eq', 'field': 'N', 'value': 'V'}
        True
        >>> a = KiiClause.equals("N", 123)
        >>> a.toDict() == {'type': 'eq', 'field': 'N', 'value': 123}
        True
        """
        return KiiClause('eq', field=field, value=value)

    @staticmethod
    def greaterThan(field, value, included):
        """
        >>> a = KiiClause.greaterThan("f", 100, True)
        >>> a.toDict() == {'type': 'range', 'field': 'f', 'lowerLimit': 100, 'lowerIncluded': True}
        True
        """
        return KiiClause('range', field=field, lowerLimit=value, lowerIncluded=included)

    @staticmethod
    def lessThan(field, value, included):
        """
        >>> a = KiiClause.lessThan("f", 200, False)
        >>> a.toDict() == {'type': 'range', 'field': 'f', 'upperLimit': 200, 'upperIncluded': False}
        True
        """
        return KiiClause('range', field=field, upperLimit=value, upperIncluded=included)

    @staticmethod
    def range(field, lowerValue, lowerIncluded, upperValue, upperIncluded):
        """
        >>> a = KiiClause.range("f", 200, False, 500, True)
        >>> a.toDict() == {'type': 'range', 'field': 'f', 'lowerLimit': 200, 'lowerIncluded':False, 'upperLimit': 500, 'upperIncluded': True}
        True
        """
        return KiiClause('range', field=field, lowerLimit=lowerValue, lowerIncluded=lowerIncluded, upperLimit=upperValue, upperIncluded=upperIncluded)

    @staticmethod
    def inClause(field, values):
        """
        >>> a = KiiClause.inClause("f", [1,2,3,5,8,13])
        >>> a.toDict() == {'type': 'in', 'field': 'f', 'values': [1,2,3,5,8,13]}
        True
        """
        return KiiClause("in", field=field, values=values)

    @staticmethod
    def notClause(clause):
        """
        >>> a = KiiClause.notClause(KiiClause.equals("a", 100))
        >>> a.toDict() == {'type': 'not', 'clause': {'type': 'eq', 'field': 'a', 'value': 100}}
        True
        """
        return KiiClause('not', clause=clause)

    @staticmethod
    def andClause(clauses):
        """
        >>> a = KiiClause.andClause([KiiClause.equals("a", 100), KiiClause.equals("b", 200)])
        >>> a.toDict() == {'type': 'and', 'clauses': [{'type': 'eq', 'field': 'a', 'value': 100}, {'type':'eq', 'field':'b', 'value':200}]}
        True
        """
        return KiiClause('and', clauses=clauses)

    @staticmethod
    def orClause(clauses):
        """
        >>> a = KiiClause.orClause([KiiClause.equals("a", 100), KiiClause.equals("b", 200)])
        >>> a.toDict() == {'type': 'or', 'clauses': [{'type': 'eq', 'field': 'a', 'value': 100}, {'type':'eq', 'field':'b', 'value':200}]}
        True
        """
        return KiiClause('or', clauses=clauses)

def doctest():
    import doctest
    doctest.testmod()
