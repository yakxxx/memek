import unittest 
from crawler.comment_crawler import *
from crawler.conf import *
from common.models import *
import mongoengine
mongoengine.connect(DB_NAME+'_tests')
from mock import *


class TestCommentCrawler(unittest.TestCase):
    
    def setUp(self):
        Article.drop_collection()
        Comment.drop_collection()
        
        a = Article(article_id='1111', title='asd',
                url = 'http://www.wykop.pl/link/1369645/trollujacy-ptak/')
        a.save()
        
        b = Article(article_id='2222', title='xxaxa',
                url = 'http://www.wykop.pl/ramka/1369071/zycie-przestepcze-w-przedwojennej-polsce/')
        b.save()
        
        
    def test_run(self):
        crawl = CommentCrawler()
        crawl.a.get_comments = Mock(side_effect=[
                                            [ 
                                              Comment(body='aaaaa', comment_id=123),
                                              Comment(body='bbbbb', comment_id=124)
                                            ],
                                            
                                            [ 
                                              Comment(body='aaaaa', comment_id=125),
                                              Comment(body='bbbbb', comment_id=126)
                                            ]
                                                ])
        crawl.run()
        self.assertEqual(Comment.objects.count(), 4)


    
    
    