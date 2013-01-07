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
                                              {'body':'aaaaa', 'comment_id':123},
                                              {'body':'bbbbb', 'comment_id':124}
                                            ],
                                            
                                            [ 
                                              {'body':'aaaaa', 'comment_id':125},
                                              {'body':'bbbbb', 'comment_id':126}
                                            ]
                                                ])
        crawl.run()
        self.assertEqual(Comment.objects.count(), 4)
        c123 = Comment.objects.get(comment_id=123)
        self.assertEqual(c123.article.article_id, 1111)
        self.assertTrue(c123.article.comments_crawled)
        
        
    def test_run_with_errors(self):
        url = 'http://www.wykop.pl/ramka/1369071/zycie-przestepcze-w-przedwojennej-polsce/'
        [Article(url = url, article_id=6666+i).save() for i in xrange(1000)]
        crawl = CommentCrawler()
        crawl.a.get_comments = Mock(side_effect=ApiError)
        crawl.run()
        self.assertEqual(crawl._err_count, 21)
        
    
    