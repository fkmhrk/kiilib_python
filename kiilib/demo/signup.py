#!/usr/bin/python
import sys
# Python Tutorial 6.1.2. "The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path."
sys.path.append(sys.path[0] + "/../..")
import kiilib

from config import *

def main():
    context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
    app_api = kiilib.AppAPI(context)

    data = {
        'age' : 29
        }
    user = app_api.signup('fkmtest', 'password1234', **data)
    print 'user = %s' % user

if __name__ == '__main__':
    main()

