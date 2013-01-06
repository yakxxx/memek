import unittest
import requests as req
from crawler.conf import *

class WykopTest(unittest.TestCase):    

    @unittest.skip
    def test_get_promoted_pages(self):
        ret_0 = req.get(API_URL+'links/promoted/appkey,'+APP_KEY+',page,1,output,clear')
        ret = req.get(API_URL+'links/promoted/appkey,'+APP_KEY+',output,clear')
        self.assertListEqual(ret_0.json, ret.json) # Page numbers start from 1
        pprint(ret.json)
    
    @unittest.skip    
    def test_get_comments(self):
        ret = req.get(API_URL+'link/comments/1362863/appkey,'+APP_KEY+',output,clear')
        pprint(ret.json)
        
#    @unittest.skip    
    def test_get_promoted_to_big_pageno(self):
        ret = req.get(API_URL+'links/promoted/appkey,'+APP_KEY+',page,999999,output,clear')
        self.assertEqual(ret.status_code, 200)
        self.assertListEqual(ret.json, [])
    
    
    
    
    