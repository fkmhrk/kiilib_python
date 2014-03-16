import unittest

from client import *
import kiilib

APP_ID = 'appId'
APP_KEY = 'appKey'
BASE_URL = 'https://api.kii.com/api'

class ExampleTest(unittest.TestCase):
    def setUp(self):
        self.factory = MockClientFactory()
        self.context = kiilib.KiiContext(APP_ID, APP_KEY, BASE_URL)
        self.context.factory = self.factory
        self.app_api = kiilib.AppAPI(self.context)
        
    def test_0000_refresh_ok(self):
        bucket = kiilib.KiiBucket(kiilib.KiiApp(), 'test')
        obj = kiilib.KiiObject(bucket, 'id1234')

        # set response
        self.factory.client.responses.append(
            MockResponse(200, {}, u'{"name":"fkm"}'))
        self.app_api.objectAPI.refresh(obj)
        
        #assertion
        self.assertEqual(u'fkm', obj['name'])
        self.assertEqual('id1234', obj.id)

    def test_0010_refresh_404(self):
        bucket = kiilib.KiiBucket(kiilib.KiiApp(), 'test')
        obj = kiilib.KiiObject(bucket, 'id1234')

        # set response
        self.factory.client.responses.append(
            MockResponse(404, {}, u'{"errorCode":"OBJECT_NOT_FOUND"}'))
        try:
            self.app_api.objectAPI.refresh(obj)
            self.fail()
        except kiilib.CloudException as e:
            #assertion
            self.assertEqual(404, e.code)
        


        
        
