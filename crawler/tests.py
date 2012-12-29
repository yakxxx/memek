#coding: utf-8
import unittest
import requests as req
from conf import *
from pprint import pprint
from mock import Mock
from api_client import *



class ApiTest(unittest.TestCase):
    
    def test_make_api_params_str(self):
        a = Api()
        api_str = a._make_api_params_str({'a':1, 'b': 'asd'})
        self.assertTrue(api_str == u'a,1,b,asd' or api_str == u'b,asd,a,1')
        
        api_str2 = a._make_api_params_str({})
        self.assertEqual(api_str2, '')
    
    def test_make_method_params(self):
        a = Api()
        ret = a._make_method_params_str(['asd','xxx',123])
        self.assertEqual(ret, u'asd/xxx/123')
        
    def test_bad_get(self):
        a = Api()
        self.assertRaises(ApiError, a._get, 'bla', ['a',1,2], {'ax':123,'by':'qqq'})
        
    def test_is_resp_ok(self):
        resp = Mock()
        a = Api()
        resp.status_code = 200
        resp.json = {'error': {'code': 1, 'message': 'xaxaxa'}}
        self.assertFalse(a._is_resp_ok(resp))

        #False
        resp.reset_mock()
        resp.status_code = 404
        resp.json = ''
        self.assertFalse(a._is_resp_ok(resp))
        
        resp.reset_mock()
        resp.status_code = 404
        resp.json = [1,2,3,4]
        self.assertFalse(a._is_resp_ok(resp))
    
        #True
        resp.reset_mock()
        resp.status_code = 200
        resp.json = [1,2,3,4]
        self.assertTrue(a._is_resp_ok(resp))
        
    def test_get_promoted(self):
        a = Api()
        promoted = a.get_promoted()
        reference = req.get(API_URL+'links/promoted/appkey,'+APP_KEY)
        self.assertListEqual(promoted, reference.json)
    
class WykopTest(unittest.TestCase):    

    def test_get_promoted_pages(self):
        ret_0 = req.get(API_URL+'links/promoted/appkey,'+APP_KEY+',page,1')
        ret = req.get(API_URL+'links/promoted/appkey,'+APP_KEY)
        self.assertListEqual(ret_0.json, ret.json) # Page numbers start from 0
        
        
    