#coding: utf-8
import sys
sys.path.append('../..')
from miner.texter import *
from common.conf import *
import mongoengine
from datetime import datetime, timedelta
import codecs

if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    arg = list(sys.argv)
    arg = [int(i) for i in arg[1:]]

    start = datetime(*arg[0:3])
    stop = start + timedelta(days=7)
    text = 'PLACEHOLDER'
    count = 0
    while len(text) > 0:
        texter = Texter(start, stop)
        texter.create_corpus()
        text = texter.text
        start=stop
        stop=start + timedelta(days=7)
        count += 1
        f = codecs.open('weeks/%d.txt' % count, 'w', 'utf-8')
        f.write(text)
        f.close()
        print 'week %d processed and saved' % count