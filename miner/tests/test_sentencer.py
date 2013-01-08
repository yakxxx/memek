#coding: utf-8
import unittest
from miner.sentencer import *
from common.models import *


class TestSentencer(unittest.TestCase):
    
    def setUp(self):
        self.s = Sentencer()
    
    def test_break_text(self):
        resp = self.s._break_to_sentences(u'Może jutro ta dama > sama da tortu jeżom. A gdybym zgolił wąs.')
        self.assertListEqual(resp, [u"Może jutro ta dama ",
                                    u" sama da tortu jeżom",
                                    u" A gdybym zgolił wąs"])
        
        resp = self.s._break_to_sentences(u'Ja cię xD ale to jest fajnie')
        self.assertListEqual(resp, [u'Ja cię ', u' ale to jest fajnie'])

        resp = self.s._break_to_sentences(u'Ja cię :3 ale to jest fajnie')
        self.assertListEqual(resp, [u'Ja cię ', u' ale to jest fajnie'])

    