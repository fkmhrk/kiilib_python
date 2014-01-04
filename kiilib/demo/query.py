#!/usr/bin/python
import sys
import os
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
from kiilib import *

from config import *

def main():
    context = kii.KiiContext(APP_ID, APP_KEY, BASE_URL)
    api = kii.AppAPI(context)
    
    user = api.login('fkmtest', 'password1234')
    print 'access token = %s' % (context.access_token)

    # create object
    bucket = kii.KiiBucket(user, 'images')
    objs = api.bucketAPI.query(bucket, kii.bucket.KiiCondition(kii.bucket.KiiClause.all()))
    for o in objs:
        print str(o)

if __name__ == '__main__':
    main()

