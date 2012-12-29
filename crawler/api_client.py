#coding: utf-8
import requests as req
from conf import *
import logging

class Api(object):


    def get_promoted(self, page=1):
        
        return self._get('links/promoted', api_params = {'appkey': APP_KEY, 'page': page})
        
        
    def _get(self, url, method_params=[], api_params={}):
        
        full_url = API_URL + url + '/' + self._make_method_params_str(method_params) \
                       + '/' + self._make_api_params_str(api_params)
        ret = req.get(full_url)
        
        if not self._is_resp_ok(ret):
            logging.error('BAD RESPONSE: full_url: ' + full_url + "\n method_params: " + unicode(method_params) \
                           + "\n api_params: " + unicode(api_params)+ "\n response: "+ unicode(ret.content))
            raise ApiError('Bad Response')
        
        return ret.json

    
    def _make_method_params_str(self, method_params):
        if method_params:
            return '/'.join([unicode(param) for param in method_params])
        else:
            return ''
        
    def _make_api_params_str(self, api_params):
        return ','.join([unicode(k)+','+unicode(v) for k,v in api_params.items()])


    def _is_resp_ok(self, resp):
        if resp.status_code == 200:
            if type(resp.json) == dict:
                return not resp.json.get('error', False)
            else:
                return True
        else:
            return False


class ApiError(Exception):
    pass