#coding: utf-8
import sys
sys.path.append('../..')
from miner.texter import *
from common.conf import *
import mongoengine
from datetime import datetime
from miner.sentencer import *

if __name__ == "__main__":
    arg = list(sys.argv)
    arg = [int(i) for i in arg[1:]]
    print arg
    db = mongoengine.connect(DB_NAME)
    texter = Texter(datetime(*arg[0:3]), datetime(*arg[3:6]))
    text = texter.create_corpus()
    text = Sentencer._clear_text(text)
    print text
    print '***********'
    print len(text)