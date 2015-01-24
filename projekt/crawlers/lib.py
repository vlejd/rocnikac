import string
from bs4 import BeautifulSoup
import requests
import pprint
import sys,os
import time
reload(sys)  
sys.setdefaultencoding('utf8')


def get_url(koho):
  r = requests.get(koho)
  return r.text

def justchars(what):
    return ''.join([x for x in what.lower() if x in string.ascii_letters])
