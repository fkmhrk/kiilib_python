#!/usr/bin/python
import sys
sys.path.append('../src')
from kiilib import *

from config import *

def main():
    context = kii.KiiContext(APP_ID, APP_KEY, BASE_URL)
    app_api = kii.AppAPI(context)
    
    user = app_api.login('fkmtest', 'password1234')
    print 'access token = %s' % (context.access_token)
    print 'user id = %s' % (user.id)

if __name__ == '__main__':
    main()

