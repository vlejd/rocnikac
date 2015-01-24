execfile("lib.py")
url= """http://people.ksp.sk/~vlejd/projekt.html"""

soup = BeautifulSoup(get_url(url))
print soup.select('div')
print "vlejd"