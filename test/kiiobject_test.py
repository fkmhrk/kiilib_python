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

    def test_0100_create_ok(self):
        bucket = kiilib.KiiBucket(kiilib.KiiApp(), 'test')
        data = {
            'name' : u'fkm',
            'score' : 120
        }

        # set response
        self.factory.client.responses.append(
            MockResponse(201, {}, u'{' +
			'"objectID":"d8dc9f29-0fb9-48be-a80c-ec60fddedb54",' +
			'"createdAt":1337039114613,' +
			'"dataType":"application/vnd.sandobx.mydata+json"' +
			'}'))
        obj = self.app_api.objectAPI.create(bucket, **data)
        
        #assertion
        self.assertEqual(u'fkm', obj['name'])
        self.assertEqual(120, obj['score'])        
        self.assertEqual('d8dc9f29-0fb9-48be-a80c-ec60fddedb54', obj.id)

    def test_0200_update_ok(self):
        bucket = kiilib.KiiBucket(kiilib.KiiApp(), 'test')
        obj = kiilib.KiiObject(bucket, 'id1234')
        
        obj['score'] = 230
        # set response
        self.factory.client.responses.append(
            MockResponse(200, {}, u'{"modifiedAt":2233}'))
        self.app_api.objectAPI.save(obj)
        
        #assertion
        request = self.factory.client.requests[0]
        self.assertEqual('https://api.kii.com/api/apps/appId/buckets/test/objects/id1234', request.url)
        self.assertEqual('PUT', request.method)
        self.assertEqual(2233, obj['_modified'])

    def test_0300_delete_ok(self):
        bucket = kiilib.KiiBucket(kiilib.KiiApp(), 'test')
        obj = kiilib.KiiObject(bucket, 'id1234')
        
        # set response
        self.factory.client.responses.append(
            MockResponse(204, {}, u''))
        self.app_api.objectAPI.delete(obj)
        
        #assertion
        request = self.factory.client.requests[0]
        self.assertEqual('https://api.kii.com/api/apps/appId/buckets/test/objects/id1234', request.url)        
        self.assertEqual("DELETE", request.method) 
        
        
