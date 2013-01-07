#coding: utf-8


from crawler.comment_crawler import *
from crawler.conf import *
import mongoengine


if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    crawler = CommentCrawler(10)
    crawler.run()
