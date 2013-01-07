#coding: utf-8

from common.models import *
from crawler.api_client import *
import logging
from pprint import pprint


class CommentCrawler(object):

    def __init__(self):
        self.a = Api()

    def run(self):
        for a in Article.objects.all():
            if a.comments_crawled:
                continue
             
            try:
                comments = self.a.get_comments(Api.parse_link_id_from_url(a.url))
            except (WrongData, ApiError) as e:
                logging.warn('Ignoring link')
                continue
            for comment in comments:
                comment.article = a
                comment.save()
  