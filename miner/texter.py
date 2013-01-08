from common.models import *
from common.conf import *

class Texter(object):
    '''Creates text corpus out of data in DB'''
    
    def __init__(self, date_start, date_end):
        self._date_start = date_start
        self._date_end = date_end
        
    def create_corpus(self):
        text_list = []
        qs = self._in_date_range_queryset()
        for article in qs:
            text_list += self._make_corpus_of_article(article) 
        return ' '.join(text_list)
    
    def _make_corpus_of_article(self, article):
        text_list = []
        if article.title:
            text_list.append(article.title)
        if article.description:
            text_list.append(article.description)
        text_list = text_list + self._make_corpus_of_comments(article)
        return text_list
        
    def _make_corpus_of_comments(self, article):
        comments = Comment.objects.filter(article=article)
        text_list = []
        for comment in comments:
            if comment.body:
                text_list.append(comment.body)
        return text_list
    
    def _in_date_range_queryset(self):
        return Article.objects.filter(date__gt=self._date_start, date__lt=self._date_end)