execfile("lib.py")
f=  open("vystup",'w')
f.write(str(sys.argv))
f.close()


js = getlinefromlist(sys.argv[1])

soup = BeautifulSoup(get_html(js['url']))
#pprint.pprint(soup)


items = soup.select(".news-latest-item")

#co, kto , link, popis, kedy, kde, raw

all_data = []
for x in items:
  d = tmplt()
  d['raw'] = x.prettify()
  d['extractor'] = js
  #if True:
  try:
    d['url'] = "http://www.fmph.uniba.sk/"+x.select("h2")[0].a.get("href")
    h = x.select("h2")[0].a.get("title")
    
    if "-" in h:
      d['co']=h.split('-')[0]
      d['kto'] = h.split('-')[1].split('(')[0]
    else:
      d['co']=h.split('(')[0]
    
  except:
    print "dab1"
  
  try:
    info = x.select("p.bodytext")[0]
    datum = re.search(r"\d\d?\.\d\d?\.\d\d\d\d",info.text)
    if datum:
      d['kedy'] = map(int, datum.group(0).split(".")[::-1])
    cas = re.search(r"\d\d?:\d\d? hod\.",info.text)
    if cas:
      d['okolkej'] = map(int,cas.group(0).split()[0].split(":"))
    
    if not ( cas and datum ):
      d['popis']=info.text
    
    if( "v miestnosti") in info.text:
      pom  = info.text.split("v miestnosti")
      if len(pom) > 0:
	d['kde'] = pom[-1].strip().split(' ')[0]
    
  except:
    print "dab2"
  
  all_data.append(d)

#savnisadade
with open("jsons/"+js['seed'],'w') as f:
  json.dump(all_data,f)

