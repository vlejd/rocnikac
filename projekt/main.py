execfile("crawlers/lib.py")
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
import sys,os
import time
import traceback
from pynliner import *
import urllib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from flask.ext.cors import CORS



app = Flask(__name__)
cors = CORS(app)
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")



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
    for data in d:
      data['raw'] = unicode(BeautifulSoup(unicode(data['raw'])).prettify())
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
  print "niekto adduje pagu"
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
  
@app.route('/api/picker',methods=['POST'])
def picker():
  form = request.form
  url = form['site']
  dis = True
  display = None
  if dis:
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
  #url= 'http://www.psychologia.sav.sk/sp/'
  #url = 'https://ib.vub.sk/ibr/login'
  #url= 'http://moja.uniba.sk'
  #url= 'http://9gag.com'
  browser = webdriver.Firefox()
  print "loading page"
  browser.get(url)
  print "loaded"
  time.sleep(1)
  url = browser.current_url;
  print "redirect to:"+url
  pom = browser.page_source
  browser.close()
  
  #req = urllib2.Request(url)
  #response = urllib2.urlopen(req)
  #pom = response.read()

  
  if dis:
    display.stop()
  soup = BeautifulSoup(pom)
  
      
  #zaby vsetky skripty
  skripts = soup.findAll("script")
  for x in skripts:
    x.decompose()
  
  bases = soup.findAll("base")
  if len(bases)==0:
    headstaff = BeautifulSoup("<base href=\""+url+"\" target=\"_blank\" ></base> <script src=\"//code.jquery.com/jquery-1.11.3.min.js\"></script> <script src=\"//code.jquery.com/jquery-migrate-1.2.1.min.js\"></script>""")
    soup.head.insert(0,headstaff)
  raw_skript = """<script type="text/javascript">
var site = \""""+url +"""\";
console.log(site);
function get_selector(el){
var selector = "";
var som = $(el);
while($(som.parent()).length!=0){
  var tagname = $(som)[0].tagName;
  var par = $(som.parent());
  var kolko = 0;
  
  if(tagname!="HTML"){
    if(tagname!="BODY"){
      kolko = par.children(tagname).index($(som))+1;
      tagname= tagname+":nth-of-type("+kolko+")";
    }
  }
  selector = tagname+" "+selector;
  som = par;
}
return selector;
}

document.onkeydown = function(e){
  console.log(e.keyCode);
  if(e.keyCode==109){
    if(selected!=0){
      selected.css({"border-style":"none"}); 
    }
    selected = old;
    selected.css({"border-color": "#FF0000", 
                "border-weight":"10px", 
                "border-style":"solid"});
    
    
  }
  if(e.keyCode==107){
    
    if(selected!=0){
      selected.css({"border-style":"none"}); 
    }
    old = selected;
    selected = selected.parent();
    selected.css({"border-color": "#FF0000", 
                "border-weight":"10px", 
                "border-style":"solid"});

  } 
  if(e.keyCode==13){
    var kam = window.location.href.replace("/api/picker","");
    
    $.ajax({
      method: "POST",
      url: kam+"/api/picked",
      data: { element: get_selector(selected), site: site },
      success: function(){
        var redir = window.location.href.replace("/api/picker","");
        window.location = redir+"/sites";
      }
    })
  } 
  console.log(get_selector($(selected)));
}
var selected=0;
var old = 0;
var pom = document.getElementsByTagName("*");
for(var i =0; i != pom.length; i++){
  pom[i].onclick = function(e){
e.preventDefault();
e.stopPropagation();
if(selected!=0){
  selected.css({"border-style":"none"});
}
old = selected;
selected = $(e.target);
selected.css({"border-color": "#FF0000", 
             "border-weight":"10px", 
             "border-style":"solid"});
console.log(get_selector($(e.target)));

}; 
}
console.log("here");

</script>"""
  print raw_skript
  skript = BeautifulSoup(raw_skript)
  print "WW"
  soup.find("html").append(skript)
  print "WW"
  ret = soup.prettify()
  
  return ret
  
@app.route('/api/picked',methods=['POST'])
def picked():
  print "niekto pickol"
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
    app.run(host='0.0.0.0',port=5000)

