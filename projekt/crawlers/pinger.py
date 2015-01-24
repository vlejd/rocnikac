execfile("lib.py")
def main():
  while True:
    f = open("list",'r')
    data = f.read().strip().split('\n')
    f.close()
    for d in data:
      stranka,program = d.split()
      print stranka,program
      #vyrob subor na logovanie, ak este nie je
      if not os.path.exists("archiv/"+justchars(stranka)):
	f = open("archiv/"+justchars(stranka),'w')
	f.close()
      f = open("archiv/"+justchars(stranka),'r')
      text = f.read()
      f.close()
      n_text = get_url(stranka)
      if( text.strip() != n_text.strip()):
	print "nieco sa zmenilo"
	execfile(program)#poextrahuj zmenenu stranku
	#zapis, ako teraz vyzera nova stranka
	f = open("archiv/"+justchars(stranka),'w')
	f.write(n_text)
	f.close()
      else:
	#nic sa nestalo
	pass
    #trosku si otdychni
    time.sleep(10)
    #time.sleep(60*60*24)

if __name__ == '__main__':
  main()