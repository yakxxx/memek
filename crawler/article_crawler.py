#coding: utf-8

from common.models import *
from crawler.api_client import *
import logging
import time
from pprint import pprint

class ArticleCrawler(object):
    
    def __init__(self, pages_limit=9999999):
        self.pages_limit = pages_limit
        self.pages_count = 1
        self.err_count = 0
        self.crawled_before_count = 0
        self.a = Api()
        
    def run(self):
        a = self.a
        while self.pages_count < self.pages_limit and self.crawled_before_count < 100:
            self._handle_err_count()   
            
            try:
                promoted = a.get_promoted(self.pages_count)
            except (WrongData, ApiError) as e:
                logging.warn('Retrying....')
                self.err_count += 1
                continue
            
            if not promoted:
                break
            
            self._save_promoted(promoted)
            
            self.err_count = 0
            self.pages_count += 1
            
        if self.crawled_before_count >= 100:
            logging.info("Stopped due to crawling previously crawled content")
            
        if self.pages_count >= self.pages_limit:
            logging.info("Stopped due to pages_limit")
            
        if promoted == []:
            logging.info("Stopped due to no more articles") 
            
    def _handle_err_count(self):
        if self.err_count > 3:
            raise CrawlerError('to many retries on page %d' % self.pages_count)
        if self.err_count > 1:
            time.sleep(0.5 * self.err_count)
            
    def _save_promoted(self, promoted):
        for p in promoted:
            art = Article(**p)
            if Article.objects.filter(article_id=art.article_id).count() == 0:
                art.save()
                self.crawled_before_count -= 1
            else:
                self.crawled_before_count += 1


class CrawlerError(Exception):
    pass


