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
    obj = api.objectAPI.create(bucket, {})
    print 'object id = %s' % (obj.id)

    # upload body
    filePath = sys.path[0] + '/image.jpg'
    api.objectAPI.updateBody(obj, 'image/jpeg',
                      open(filePath, 'rb'), os.path.getsize(filePath))
    print 'file uploaded'

    # download body
    with open('downloaded.jpg', 'wb') as target:
        api.objectAPI.downloadBody(obj, target)
        print 'file downloaded'


if __name__ == '__main__':
    main()

