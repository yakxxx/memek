#coding: utf-8
import sys
import os
from miner.collocator import *
from common.conf import *
import mongoengine
from datetime import datetime, timedelta, date
import codecs
from nltk.tokenize import wordpunct_tokenize
import itertools
from math import log, floor


def load_words(no, weeks_dir):
    f = codecs.open(weeks_dir+'/%d.txt' % no,'r','utf-8')
    text = f.read()
    f.close()
    return wordpunct_tokenize(text)

def smart_duplicate_remove(colloc_set):
    generated_bigram_list = []
    selected_bigram_list = []
    selected_trigram_list = []
    for col in colloc_set:
        if len(col) == 3:
            selected_trigram_list.append(col)
            generated_bigram_list.append((col[0], col[1]))
            generated_bigram_list.append((col[0], col[2]))
            generated_bigram_list.append((col[1], col[2]))
        else:
            selected_bigram_list.append(col)
    
    return (set(selected_bigram_list) - set(generated_bigram_list)).union(set(selected_trigram_list))

def zeitgeist(max_week, weeks_dir):
    ref_words = []
    out = codecs.open('output.txt', 'w', 'utf-8')
    
    for i in xrange(1, 5):
        ref_words.append(load_words(i, weeks_dir))
    
    for i in xrange(5, max_week + 1):
        words_big = list(itertools.chain(*ref_words))
        words = load_words(i, weeks_dir)
        if len(words) == 0:
            break
        c_big = Collocator(words_big)
        c_small = Collocator(words)
    
        freq_filter = lambda words_len: floor(log(words_len, 2) - 9.5)
        freq_filter_big = freq_filter(len(words_big)) 
        freq_filter_small = freq_filter(len(words)) + 1
        collocations_big = c_big.find_collocations(freq_filter_big)
        collocations_small = c_small.find_collocations(freq_filter_small)

        set_big = set(collocations_big)
        set_small = set(collocations_small)
    
        memes = set_small - set_big
        memes = smart_duplicate_remove(memes)
        
        line = ';'.join([unicode(date(2011,1,1) + timedelta(days=7*(i-1))),
                        unicode(date(2011,1,1) + timedelta(days=7*(i)))])
        
        for mem in memes:
            line = ';'.join([line, ' '.join(mem)])
        line += '\n'
        out.write(line)
        sys.stdout.write('.')
                
        ref_words.append(words)
        del ref_words[0]

    sys.stdout.write('\n')
    out.close()

if __name__ == "__main__":
    db = mongoengine.connect(DB_NAME)
    max_week = int(sys.argv[1])
    weeks_path = sys.argv[2]
    zeitgeist(max_week, weeks_path)
    
