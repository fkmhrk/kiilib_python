
class KiiBucket:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def getPath(self):
        return '%s/buckets/%s' % (self.owner.getPath(), self.name)

