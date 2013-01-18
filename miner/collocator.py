#coding: utf-8
import nltk
from nltk.collocations import *
import re
import codecs
import logging
import os

class Collocator(object):
    
    def __init__(self, words):
        self.words = words
        path = os.path.dirname(__file__)
        f = codecs.open(os.path.join(path,'stopwords.txt'), 'r', 'utf-8')
        stop_words = f.read()
        f.close()
        
        self._stop_words = set(stop_words.split(', '))


    def find_collocations(self, freq_filter=10):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        trigram_measures = nltk.collocations.TrigramAssocMeasures()

        finder = BigramCollocationFinder.from_words(self.words)
        finder.apply_freq_filter(freq_filter)
        finder.apply_word_filter(lambda w: len(w) < 4 or w in self._stop_words)
        finder.apply_ngram_filter(lambda w1, w2: len(w1) + len(w2) < 10)
        best_bigrams = finder.nbest(bigram_measures.chi_sq, 100000) 
        
        finder3 = TrigramCollocationFinder.from_words(self.words)
        finder3.apply_freq_filter(freq_filter)
        finder3.apply_word_filter(lambda w: len(w) < 4 or w in self._stop_words)
        finder3.apply_ngram_filter(lambda w1, w2, w3: len(w1) + len(w2) + len(w3) < 13)
        best_trigrams = finder3.nbest(trigram_measures.chi_sq, 100000) 
         
        
        return best_bigrams + best_trigrams
