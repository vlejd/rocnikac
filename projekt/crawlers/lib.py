import string
from bs4 import BeautifulSoup
import requests
import pprint
import sys,os
import re
import subprocess
import time
import json
import sys
from pyvirtualdisplay import Display
from selenium import webdriver

reload(sys)  
sys.setdefaultencoding('utf8')

def tmplt():
  pom = {}
  pom['kto']=None
  pom['co']=None
  pom['kedy']=None
  pom['okolkej']=None
  pom['kde']=None
  pom['url']=None
  pom['popis']=None
  pom['raw']=None
  pom['extractor'] = None
  return pom

def code(x):
  return URLEncoder.encode(url, "UTF-8");

def getlinefromlist(x):
  f = open("list",'r')
  js = json.loads(f.read().split('\n')[int(x)])
  f.close()
  return js

def get_html(koho):
  r = requests.get(koho)
  return r.text

def justchars(what):
    return ''.join([x for x in what.lower() if x in string.ascii_letters])
