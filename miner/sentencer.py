from nltk.tokenize import sent_tokenize, RegexpTokenizer
import re

class Sentencer(object):
    
    def _break_to_sentences(self, text):
        text = re.sub(r'(:[a-zA-Z0-9])|(x[A-Z])', ';', text)
        tokenizer = RegexpTokenizer(r'[\w\s]+')
        return tokenizer.tokenize(text)