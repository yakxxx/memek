#coding: utf-8

from common.models import *
from crawler.api_client import *
import logging
from pprint import pprint

class CommentCrawler(object):

    def __init__(self, limit=9999999):
        self.a = Api()
        self._err_count = 1
        self._limit = limit
        self.MAX_ERRORS = 20

    def run(self):
        query_set =  Article.objects.filter(comments_crawled=False)
        oldest = Article.objects.order_by('-date').limit(1)[0]
        logging.info("%s articles found, last from %s" % (query_set.count(), oldest.date))
        
        article_count = 0
        
        for a in query_set:
            if self._err_count > self.MAX_ERRORS:
                break
            
            if article_count > self._limit:
                break
             
            try:
                comments = self.a.get_comments(Api.parse_link_id_from_url(a.url))
            except (WrongData, ApiError) as e:
                logging.warn('Ignoring article %s' % a.url)
                self._err_count += 1
                continue
            
            self._handle_err_count()
            article_count +=1
            
            for comment in comments:
                obj = Comment(**comment)
                obj.article = a
                obj.save()
                
            a.comments_crawled = True
            a.save()
        
        if self._err_count > self.MAX_ERRORS:
            logging.info('Stopped due to to many errors')
            
        if article_count > self._limit:
            logging.info('Stopped due to article limit')

    def _handle_err_count(self):
        if self._err_count > 0:
            self._err_count -= 1