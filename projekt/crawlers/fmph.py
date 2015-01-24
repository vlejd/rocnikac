execfile("lib.py")
url= """http://www.fmph.uniba.sk/index.php?id=kalendar"""
soup = BeautifulSoup(get_url(url))
#pprint.pprint(soup)
print "fmph"