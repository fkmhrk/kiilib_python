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
    bucket = kiilib.KiiBucket(user, 'images')
    condition = kiilib.KiiCondition(clause = kiilib.KiiClause.all(),
                                    limit = 1)
    while True:
        objs = api.bucketAPI.query(bucket, condition)
        for o in objs:
            print str(o)
        if condition.hasNext() == False:
            break

if __name__ == '__main__':
    main()

