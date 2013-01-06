#coding: utf-8
import unittest
import requests as req
import re
from crawler.conf import *
from mock import Mock
from pprint import pprint

from crawler.api_client import *
from common.models import *

import mongoengine

mongoengine.connect(DB_NAME+'_tests')

class ApiTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(ApiTest, self).__init__(*args, **kwargs)
        a = Api()
        self.promoted = a.get_promoted()
        
    def setUp(self):
        self.a = Api()
        Article.drop_collection()
        Comment.drop_collection()
    
    def test_make_api_params_str(self):
        api_str = self.a._make_api_params_str({'a':1, 'b': 'asd'})
        self.assertTrue(api_str == u'a,1,b,asd' or api_str == u'b,asd,a,1')
        
        api_str2 = self.a._make_api_params_str({})
        self.assertEqual(api_str2, '')
    
    def test_make_method_params(self):
        ret = self.a._make_method_params_str(['asd','xxx',123])
        self.assertEqual(ret, u'asd/xxx/123')
        
    def test_bad_get(self):
        self.assertRaises(ApiError, self.a._get, 'bla', ['a',1,2], {'ax':123,'by':'qqq'})
        
    def test_is_resp_ok(self):
        resp = Mock()
        resp.status_code = 200
        resp.json = {'error': {'code': 1, 'message': 'xaxaxa'}}
        self.assertFalse(self.a._is_resp_ok(resp))

        #False
        resp.reset_mock()
        resp.status_code = 404
        resp.json = ''
        self.assertFalse(self.a._is_resp_ok(resp))
        
        resp.reset_mock()
        resp.status_code = 404
        resp.json = [1,2,3,4]
        self.assertFalse(self.a._is_resp_ok(resp))
    
        #True
        resp.reset_mock()
        resp.status_code = 200
        resp.json = [1,2,3,4]
        self.assertTrue(self.a._is_resp_ok(resp))
        
    def test_get_promoted(self):
        promoted = self.a.get_promoted()
        self.assertGreater(len(promoted[0]['title']), 0)
        
    def test_get_comments(self):
        link_id = self.a.parse_link_id_from_url(self.promoted[0]['url'])
        self.assertTrue(re.match(r'[0-9]*', link_id))

        comments = self.a.get_comments(link_id)
        self.assertGreater(len(comments), 0)
        
    def test_load_comments_into_model(self):
        link_id = self.a.parse_link_id_from_url(self.promoted[0]['url'])
        comments = self.a.get_comments(link_id)
        model_comment = Comment(**comments[0])
        self.assertEqual(model_comment.comment_id, comments[0]['id'])
      
        try:
            model_comment.save()
        except Exception as e:
            self.fail(e)
            
    def test_load_articles_into_model(self):
        art = Article(**self.promoted[0])
        self.assertEqual(art.article_id, self.promoted[0]['id'])
        
        try:
            art.save()
        except Exception as e:
            self.fail(e)
        
    def test_parse_link_id(self):
        url = u'http://www.wykop.pl/link/1363053/maszyny-ktorych-jeszcze-nie-znamy/'
        link_id = self.a.parse_link_id_from_url(url)
        self.assertEqual(link_id, '1363053')
        self.assertRaises(WrongData, self.a.parse_link_id_from_url, 'xxaxaxaxa')
        
    def test_clear_comments(self):
        comments = [{ 'date': '2012-12-30 14:49:24'}]
        self.a._clear_comments(comments)
        self.assertEqual(type(comments[0]['date']), datetime)
        
        #Will it work without leading zeros? 
        comments = [{ 'date': '2012-1-1 14:49:24'}]
        self.a._clear_comments(comments)
        self.assertEqual(type(comments[0]['date']), datetime)
        
    
    