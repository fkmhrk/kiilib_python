#!/usr/bin/python
import sys

sys.path.append(sys.path[0] + "/../..")
import kiilib

from config import *

def main():
    context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
    app_api = kiilib.AppAPI(context)

    user = app_api.login('fkmtest', 'password1234')
    app_api.userAPI.refresh(user)
    print 'name = %s' % user['name']

if __name__ == '__main__':
    main()    
