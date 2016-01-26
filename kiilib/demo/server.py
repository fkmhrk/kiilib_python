#!/usr/bin/python
import sys
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
import kiilib

from config import *

def main():
    context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
    app_api = kiilib.AppAPI(context)
    
    user = app_api.login('fkmtest', 'password1234')
    print 'access token = %s' % (context.access_token)
    print 'user id = %s' % (user.id)
    
    result = app_api.serverAPI.execute('api1', None)
    print '/api1 result = %s' % (result)

    params = {
        u'key' : u'value'
    }
    result = app_api.serverAPI.execute('echo', params)
    print '/echo result = %s' % (result)

if __name__ == '__main__':
    main()

