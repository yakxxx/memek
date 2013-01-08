#coding: utf-8
from nltk.tokenize import sent_tokenize, RegexpTokenizer
import re

class Sentencer(object):
    
    def _break_to_sentences(self, text):
        text = re.sub(r'(:[a-zA-Z0-9])|(x[A-Z])', ';', text)
        tokenizer = RegexpTokenizer(r'[\w\s]+')
        return tokenizer.tokenize(text)
    
    @classmethod
    def _clear_text(cls, text):
        #remove urls
        text = re.sub(ur'http://[a-zA-Z_\/\.]+', '', text, flags=re.UNICODE)
        #remove nick links like @yakxxx
        text = re.sub(ur'(@[a-zA-Z0-9_]+)(\s|:)', '', text, flags=re.UNICODE)
        #remove emots
        text = re.sub(ur'(:[a-zA-Z0-9])|(x[A-Z])', '', text, flags=re.UNICODE)
        #remove non allnum
        text = re.sub(ur'[^\w\s]*', '', text, flags=re.UNICODE)
        #remove new lines
        text = re.sub(u'\n', ' ', text, flags=re.UNICODE)
        #remove many whitespaces in line
        text = re.sub(ur'\s+', ' ', text, flags=re.UNICODE)
        return text