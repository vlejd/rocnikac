execfile("crawlers/lib.py")
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
import sys,os
import time
import traceback

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/manager')
def manager():
    d = []
    try:
      f = open("crawlers/list","r")
      d = map(lambda x: json.loads(x), filter(lambda x: len(x.strip())>1, f.read().strip().split('\n')))
      f.close()
      pprint.pprint(d)
    except:
      print "manager eror",sys.exc_info()
      print traceback.print_exception(*sys.exc_info())
    
    return render_template("manager.html",data=d)

@app.route('/sites')
def sited():
    d = []
    try:
      f = open("crawlers/list","r")
      d = map(lambda x: json.loads(x), filter(lambda x: len(x.strip())>1, f.read().strip().split('\n')))
      f.close()
      pprint.pprint(d)
    except:
      print "sites eror",sys.exc_info()
      print traceback.print_exception(*sys.exc_info())
    
    return render_template("sites.html",data=d)

@app.route('/site/')
@app.route('/site/<seed>')
def site(seed = None):
  if seed == None:
    return "neexistuje"
  
  if os.path.isfile("crawlers/jsons/"+seed):
    f = open("crawlers/jsons/"+seed,'r')
    d = json.load(f)
    f.close()
    for x in data:
      data['raw'] = data['raw'].prettify()
    return render_template('site.html',data=d, notraw = d[0]['extractor']['program']!= 'default.py')
  
  else:
    return "neexistuje"




@app.route('/status')
def status():
  ll = open("crawlers/log","r")
  d = ll.read()
  ll.close()
  return render_template('status.html',data=d.split("\n"));


@app.route('/api/add',methods=['POST'])
def api_add():    
    print "niekto adduja pagu"
    form = request.form
    pprint.pprint(form)
    #TODO viest si log
    
    if (len(form['site'])) > 3:
      site = form['site']
      element = 'body'
      if len(form['element'])>1:
	element = form['element']
	
      try:
	tim = time.time()
	timestamp = str(tim).split('.')[0]
	f = open("crawlers/list","a")
	print "otvorene"
	f.write("\n"+json.dumps({'url':site,'element':element , 'program': 'default.py', 'seed':timestamp}))
	f.close()
      except:
	print "nepodarilo sa"
	print "error:",sys.exc_info()
	print traceback.print_exception(*sys.exc_info())
	
    return redirect(url_for('manager'))
  
@app.route('/ping')
def ping():
    data = []
    path = "crawlers/jsons/"
    for f in os.listdir(path):
      with open(path+f,'r') as ff:
	data+=json.load(ff)
	
    return str(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
