execfile("lib.py")
url = sys.argv[1]
soup = BeautifulSoup(get_html(url))
print soup.select('div')
print "vlejd"