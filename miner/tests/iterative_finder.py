#coding: utf-8
import sys
import os
sys.path.append('../..')
from miner.collocator import *
from common.conf import *
import mongoengine
from datetime import datetime, timedelta
import codecs
from nltk.tokenize import wordpunct_tokenize
import itertools
from math import log, floor


def load_words(no):
    f = codecs.open('weeks/%d.txt' % no,'r','utf-8')
    text = f.read()
    f.close()
    return wordpunct_tokenize(text)

if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    max_week = int(sys.argv[1])
    ref_words = []
    
    for i in xrange(1, 5):
        ref_words.append(load_words(i))
    
    for i in xrange(5, max_week + 1):
        words_big = list(itertools.chain(*ref_words))
        words = load_words(i)
        if len(words) == 0:
            break
        c_big = Collocator(words_big)
        c_small = Collocator(words)
    
        freq_filter = lambda words_len: floor(log(words_len, 2) - 9.5)
        freq_filter_big = freq_filter(len(words_big)) 
        freq_filter_small = freq_filter(len(words))
        collocations_big = c_big.find_collocations(freq_filter_big)
        collocations_small = c_small.find_collocations(freq_filter_small)

        set_big = set(collocations_big)
        set_small = set(collocations_small)
    
        memes = set_small - set_big
#        print '*************SMALL*************'
#        print collocations_small
        print 'week %d - data size: %d %d %d' % (i, len(words), freq_filter_big, freq_filter_small), \
                datetime(2011,1,1) + timedelta(days=7*(i-1))
        print list(memes)
        print "\n"
        
        ref_words.append(words)
        del ref_words[0]
