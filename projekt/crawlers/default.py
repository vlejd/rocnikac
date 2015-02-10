execfile("lib.py")

js = getlinefromlist(sys.argv[1])

soup = BeautifulSoup(get_html(js['url']))

all_data = []
for el in soup.select(js['element']):
  d = tmplt()
  d['extractor'] = js
  d['url'] = js['url']
  d['raw'] = el.prettify()
  #pprint.pprint(d)
  all_data.append(d)

with open("jsons/"+js['seed'],'w') as f:
  json.dump(all_data,f)