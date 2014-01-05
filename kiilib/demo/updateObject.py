#!/usr/bin/python
import sys
import os
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
import kiilib

from config import *

def main():
    context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
    api = kiilib.AppAPI(context)
    
    user = api.login('fkmtest', 'password1234')
    print 'access token = %s' % (context.access_token)

    # create object
    bucket = kiilib.KiiBucket(user, 'address')
    obj = api.objectAPI.create(bucket, {'name': 'fkm'})
    print 'object id = %s' % (obj.id)

    # update object
    obj.data['age'] = 29
    api.objectAPI.update(obj)
    print 'object is updated'

    # get by ID
    obj2 = api.objectAPI.getById(obj.bucket, obj.id)
    print str(obj2)

if __name__ == '__main__':
    main()

