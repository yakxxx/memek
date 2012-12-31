#coding: utf-8
import requests as req
from conf import *
import logging
import re
from datetime import datetime

class Api(object):

    def get_promoted(self, page=1):
        promoted = self._get('links/promoted', api_params = self._build_api_params({'page': page}))
        self._clear_promoted(promoted)
        return promoted
    
    def get_comments(self, link_id):
        comments = self._get('link/comments/'+link_id, api_params = self._build_api_params())
        self._clear_comments(comments)
        return comments
    
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
        
    def _build_api_params(self, custom_params = {}):
        default = {  'appkey' : APP_KEY,
                     'output' : 'clear'
                   }
        default.update(custom_params)
        return default
    
    def parse_link_id_from_url(self, url):
        match = re.search(r'/link/([0-9]*)/', url)
        if match:
            return match.group(1)
        else:
            raise WrongData('url not containing link_id in proper format')
        
    def _clear_promoted(self, promoted):
        for p in promoted:
            p['date'] = datetime.strptime(p['date'], '%Y-%m-%d %H:%M:%S')
            
        return promoted

    def _clear_comments(self, comments):
        for c in comments:
            c['date'] = datetime.strptime(c['date'], '%Y-%m-%d %H:%M:%S')
        return comments
    


class ApiError(Exception):
    pass

class WrongData(Exception):
    pass