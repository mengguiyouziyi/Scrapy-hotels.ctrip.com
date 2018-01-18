import re
import urllib2
from bs4 import BeautifulSoup

re = urllib2.urlopen('http://www.hupu.com/')
html = re.read()

soup = BeautifulSoup(html,"html.parser")
print html
