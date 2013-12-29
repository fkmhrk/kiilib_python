#!/usr/bin/python
import sys
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
from kiilib import *

from config import *

def main():
    context = kii.KiiContext(APP_ID, APP_KEY, BASE_URL)
    app_api = kii.AppAPI(context)
    
    user = app_api.loginAsAdmin(CLIENT_ID, CLIENT_SECRET)
    print 'admin access token = %s' % (context.access_token)
    print 'admin user id = %s' % (user.id)

    user = app_api.login('fkmtest', 'password1234')
    print 'access token = %s' % (context.access_token)
    print 'user id = %s' % (user.id)

if __name__ == '__main__':
    main()

