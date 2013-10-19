#!/usr/bin/python
import sys
import os
sys.path.append('../src')
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
    filePath = 'image.jpg'
    api.objectAPI.updateBody(obj, 'image/jpeg',
                      open(filePath, 'rb'), os.path.getsize(filePath))
    print 'file uploaded'

    # download body
    with open('downloaded.jpg', 'wb') as target:
        api.objectAPI.downloadBody(obj, target)
        print 'file downloaded'


if __name__ == '__main__':
    main()

