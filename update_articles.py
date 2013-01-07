#!/usr/bin/python
#coding: utf-8


from crawler.article_crawler import *
from crawler.conf import *
import mongoengine


if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    crawler = ArticleCrawler()
    crawler.run()
