#coding: utf-8
import unittest
from miner.texter import *
from common.models import *
from datetime import datetime

import mongoengine
mongoengine.connect(DB_NAME+'_tests')

from mock import *

class TestTexter(unittest.TestCase):
    
    def setUp(self):
        self.t = Texter(datetime(2012, 11, 1), datetime(2012, 12, 30))
        
        a = Article(article_id=111, title=u"Stary", \
                description=u"Ten artykuł jest bardzo stary",
                date = datetime(2012, 9, 17))
        a.save()
        self.a1 = a
        
        a = Article(article_id=123, title=u"Trujące grzyby", \
                description="W lesie można znaleźć bardzo wiele trujących grzybów",
                date = datetime(2012, 11, 17))
        a.save()
        self.a2 = a
        
        c = Comment(article=a, comment_id=111, body=u"komentarzyk")
        c.save()
        
        a = Article(article_id=222, title=u"Nowy", \
                description=u"Ten artykuł jest bardzo nowy",
                date = datetime(2013, 1, 6))
        a.save()
        self.a3 = a
        
    def tearDown(self):
        Article.drop_collection()
        Comment.drop_collection()
        
    def test_create_corpus(self):
        text = self.t.create_corpus()
        self.assertGreater(len(text), 40)
        
    def test_queryset(self):
        qs = self.t._in_date_range_queryset()
        count = 0
        for a in qs:
            count += 1
            self.assertGreater(a.date, datetime(2012, 11, 1))
            self.assertLess(a.date, datetime(2012, 12, 30))
        self.assertGreater(count, 0)
            
    def test_corpus_of_comments(self):
        text_list = self.t._make_corpus_of_comments(self.a2)
        self.assertListEqual(text_list, [u"komentarzyk"])
        
    def test_corpus_of_article(self):
        text_list = self.t._make_corpus_of_article(self.a2)
        self.assertGreater(len(text_list), 0)
        