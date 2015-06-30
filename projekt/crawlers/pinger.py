execfile("lib.py")
import traceback
import datetime
def main():
  while True:
    try:
      if(not os.path.exists("list")):
        f = open("list",'w')
        f.close()
      if(not os.path.exists("archiv")):
        os.makedirs("archiv")
      
      if(not os.path.exists("jsons")):
        os.makedirs("jsons")
      
      f = open("list",'r')
      data = f.read().strip().split('\n')
      f.close()
      for i,d in enumerate(data):
        if(len(d.strip())<1): continue
      
        js = json.loads(d)
        pprint.pprint(js)
        #vyrob subor na logovanie, ak este nie je
        archiv = "archiv/"+js['seed']
        if not os.path.exists(archiv):
          f = open(archiv,'w')
          f.close()
        f = open(archiv,'r')
        text = f.read()
        f.close()
        all_text = get_html(js['url'])
        print js['element']
        soup = BeautifulSoup(all_text).select( js['element'].lower().strip())
        n_text = "".join(map(lambda x:x.prettify(),soup))
        if( text.strip() != n_text.strip()): #debug
          print "nieco sa zmenilo"
          try:
            print str(i)
            subprocess.call(["python", js['program'], str(i)])#poextrahuj zmenenu stranku
            f = open(archiv,'w')
            f.write(n_text)
            f.close()
            print "done"
          except:
            print "extract error"
        else:
          #nic sa nestalo
          pass
      #trosku si otdychni
      
    except:
      s = traceback.print_exc()
      print s
      ll = open("log","a")
      ll.write(str(datetime.datetime.now())+" "+str(s)+"\n")
      ll.close()
      
    print "sleep"
    time.sleep(1000) #debug
    print "end of sleep"
    ll = open("log","a")
    ll.write(str(datetime.datetime.now())+"\n")
    ll.close()
    #time.sleep(60*60*24)

if __name__ == '__main__':
  main()