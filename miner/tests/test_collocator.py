#coding: utf-8
import unittest
import os
import nltk
from nltk.tokenize import wordpunct_tokenize

from miner.collocator import *
from common.models import *
import codecs
from pprint import pprint


class TestCollocator(unittest.TestCase):
    
    def __init__(self, methodName='runTest'):
        path = os.path.dirname(__file__)
        f = codecs.open(os.path.join(path,'big_corpus.txt'), 'r', 'utf-8')
        self.text = f.read()
        f.close()
        self.words = wordpunct_tokenize(self.text)
        
        unittest.TestCase.__init__(self, methodName=methodName)
    
    def setUp(self):
        self.c = Collocator(self.words)
    
    def test_find_collocations(self):
        colloc = self.c.find_collocations(3)
        self.assertGreater(len(colloc), 0)
#        pprint(colloc)
        
    def test_tokenize(self):
        words = wordpunct_tokenize(u"Już nadchodzi katastrofy smoleńskiej")
        self.assertListEqual(words,[u"Już", u"nadchodzi", u"katastrofy", u"smoleńskiej"])
        
        
    def test_stopwords(self):
        self.assertGreater(len(self.c._stop_words), 0)
