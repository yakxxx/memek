from secret_config import *
import logging

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

API_URL = 'http://a.wykop.pl/'
DB_NAME = 'memek'