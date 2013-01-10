#coding: utf-8
import sys
import os
sys.path.append('../..')
from miner.collocator import *
from common.conf import *
import mongoengine
from datetime import datetime
import codecs
from nltk.tokenize import wordpunct_tokenize


if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    
    f = codecs.open(sys.argv[1],'r','utf-8')
    text_big = f.read()
    f.close()
    
    f = codecs.open(sys.argv[2],'r','utf-8')
    text_small = f.read()
    f.close()
    
    c_small = Collocator(wordpunct_tokenize(text_small))
    c_big = Collocator(wordpunct_tokenize(text_big))
    
    collocations_big = c_big.find_collocations(5)
    collocations_small = c_small.find_collocations(3)

    set_big = set(collocations_big)
    set_small = set(collocations_small)
    
    memes = set_small - set_big
    print '*************SMALL*************'
    print collocations_small
    print '*************MEMES***************'
    print list(memes)
