#!/usr/bin/python
import sys
import os
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
import kiilib

from config import *

if __name__ == "__main__":
    # CRUD an object in app-scope
    context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
    api = kiilib.AppAPI(context)
    user = api.login('fkmtest', 'password1234')
    bucket = kiilib.KiiBucket(kiilib.APP_SCOPE, "dummy")
    # create
    obj = api.objectAPI.create(bucket, name="John Doe", age=28)
    print "saved object : %s" % obj

    obj["hungry"] = True
    api.objectAPI.save(obj)
    print "updated object : %s" % obj

    api.objectAPI.refresh(obj)
    print "re-retrieved the object : %s" % obj

    api.objectAPI.delete(obj)
    print "deleted"

    print "trying to retrieve the object"
    try:
        api.objectAPI.refresh(obj)
    except kiilib.CloudException, e:
        print "failed with %s" % e



