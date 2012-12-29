import unittest
import requests as req
from conf import *
from pprint import pprint



class ApiTest(unittest.TestCase):
    pass
    
    
class WykopTest(unittest.TestCase):    

    def test_get_promoted(self):
        ret = req.get(API_URL+'links/promoted/appkey,'+APP_KEY)
        pprint(ret.json)