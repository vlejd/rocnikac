from flask import Flask, render_template, session, redirect, url_for, escape, request, send_file
from flask.ext.sqlalchemy import SQLAlchemy
import dateutil.parser
import json
import random
from collections import defaultdict
import time
import datetime
import xlwt
import json

"""
TODO: spraCOVANIE DAT
"""

# Disable caching
class MyFlask(Flask):
    def get_send_file_max_age(self, name):
      return 0
      if name.lower().endswith('.js'):
        return 60
      return Flask.get_send_file_max_age(self, name)

app = MyFlask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://savka:savka@localhost/savka'
db = SQLAlchemy(app)

other_method = [-1, 4, 3, 2, 1] 

def init_database():
    db.engine.execute(""" 
    CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    sex text,
    age int,
    demografia text,
    method int,
    method2 int,
    complete int,
    result int,
    result2 int);
    """)
    db.engine.execute(""" 
    CREATE TABLE IF NOT EXISTS data(
    id serial PRIMARY KEY,
    answer text);
    """)

    db.engine.execute(""" 
    CREATE TABLE IF NOT EXISTS method(
    id integer PRIMARY KEY,
    type text,
    count int
    );
    """)
    kolko = db.engine.execute("""SELECT count(*) from method """).fetchall();
    if kolko[0][0]==0:
        db.engine.execute("""INSERT INTO method (id,type,count) VALUES (1,'UT (distrakcia)-prenajom',0) """)
        db.engine.execute("""INSERT INTO method (id,type,count) VALUES (2,'CT (premyslanie)-prenajom',0) """)
        db.engine.execute("""INSERT INTO method (id,type,count) VALUES (3,'UT (distrakcia)-kupa',0) """)
        db.engine.execute("""INSERT INTO method (id,type,count) VALUES (4,'CT (premyslanie)-kupa',0) """)
        
    

@app.route('/')
def main():
  return render_template('index.html') 
  
def valid_age(age):
    if not age.isdigit():
        return False
    age = int(age)
    if not 0<age<130:
        return False
    return True
    
def valid_sex(sex):
    if sex in ['Muz','Zena']:
        return True
    else:
        return False

@app.route('/test',methods = ['GET','POST'])
def test():
    if request.method == 'GET':
        if 'badlogin' in session:
            session.pop('badlogin')
            return render_template('test.html', id = session['id'], wrondSubmit='true')
        
        if 'id' in session:
            return render_template('test.html', id = session['id'], duplicit = 'true')
        else:
            data = db.engine.execute(""" 
            INSERT INTO users (complete) VALUES (-1)
            RETURNING id;
            """).fetchall()
            session['id'] = data[0][0]
            
            #print debug
            return render_template('test.html', id = session['id'])
    
    if request.method == 'POST':
        
        age = request.form.get('age')
        sex = request.form.get('sex')
        
        if valid_age(age) and valid_sex(sex):
            #zisti metodu, updatni databzu a zacni riesit
            #daj random delay, nech to nie je vsetko naraz
            print
            print session['id']
            print age
            print sex
            
            #zisti, akej metody je najmenej a daj ju tam
            if 'method' in session:
                method= session['method']
            else:
                method = -1
                result = db.engine.execute("""
                UPDATE method SET count = count+1 
                WHERE id= (
                    SELECT min(id) FROM method 
                        WHERE count = (
                                SELECT min(count) FROM method
                        )
                ) 
                RETURNING id;
                """).fetchall()
                method = result[0][0]
                session['method']=method
        
            db.engine.execute("""
              UPDATE users SET age = %s, complete = 0, sex = %s, method = %s, method2 = %s
              WHERE id = %s""", str(age), str(sex), str(method), str(other_method[method]), str(session['id']))
            return render_template('actual_test.html', method = method)
        else:
            session['badlogin']=True;
            return redirect(url_for('test'))

@app.route('/api/demografia',methods=['POST'])
def save_demografia():
    dem = request.form.get('data')
#    print dem
    db.engine.execute("""
              UPDATE users SET demografia = %s
              WHERE id = %s""", dem, str(session['id']))
    return "return";
    

@app.route('/api/save',methods=['POST'])
def save_data():
    user_id = session['id']
    current_method = int(request.form.get('method'))
    complete, method, method2 = db.engine.execute("""
        SELECT complete,method,method2 FROM users WHERE id = %s""",
        user_id).fetchall()[0]
    print "comp", complete, method, method2, current_method

    if complete == 2:
      print "wut"
      return ""
    if complete == 0 and method != current_method:
      print "wut1"
      return ""
    if complete == 1 and method2 != current_method:
      print "wut2"
      return ""

#    print
    data = request.form.get('data');
#    print data
#    print
    cislo = db.engine.execute("""
      INSERT INTO data (answer) VALUES (%s)
      RETURNING id;
    """, data).fetchall()[0][0]
#    print
#    print session['id']
#    print
    if complete == 0:
      db.engine.execute("""
        UPDATE users SET complete = %s, result = %s
        WHERE id = %s""", complete+1, cislo, user_id)
    else:
      db.engine.execute("""
        UPDATE users SET complete = %s, result2 = %s
        WHERE id = %s""", complete+1, cislo, user_id)
    
    if complete == 0:
      return str(method2)
    return ""

@app.route('/end')
def koniec():
    reset();
    return render_template('end.html')

@app.route('/apirender/<what>') #NEBEZPECNE!!
def vratfile(what):
    return render_template('test/'+what+'.html')

@app.route('/api/method', methods=['get'])
def get_method():
    return str(session['method']);


@app.route('/databasereset123vesloheslo')
def droptables():
    db.engine.execute(""" DROP TABLE IF EXISTS method;""")
    db.engine.execute(""" DROP TABLE IF EXISTS users;""")
    db.engine.execute(""" DROP TABLE IF EXISTS data;""")
    init_database()
    return redirect(url_for('main'))

@app.route('/reset')
def reset(): # zmaz info o terajsej session
    if 'id' in session:
        session.pop('id')
    if 'method' in session:
        session.pop('method')
    if 'badlogin' in session:
        session.pop('badlogin')
    return redirect(url_for('main'))

def padding(di,kolko):
    big=di+['']*kolko
    return big[:kolko]
    
@app.route('/generate123sav123psychologia')
def gen_xls():
    wb = xlwt.Workbook()
    #LEGENDA METOD
    xl_met = wb.add_sheet('legenda')
    metody=db.engine.execute("""
    SELECT * FROM method;
    """).fetchall();
    metody = sorted(metody)
    xl_met.write(0,0,"id")
    xl_met.write(0,1,"Nazov metody")
    
    for i,x in enumerate(metody):
        for j,xx in enumerate(x[:-1]):
            xl_met.write(i+1,j,xx)
    
    #samotny usery
    xl_met = wb.add_sheet('vysledky')
    usery=db.engine.execute("""
    SELECT * FROM users;    
    """).fetchall();
    data=db.engine.execute("""
    SELECT * FROM data;    
    """).fetchall();
    
    usery= sorted(usery)
    datadict = {x[0]: json.loads(x[1]) for x in data}
    print str(usery);
    print str(datadict[1]);
    
    #LEGENDA dat
    legend = ["id","pohlavie","vek"]+["demografia "+str(q+1) for q in xrange(7+4)] + ["Ako sa rozhodli"]+ ["Kedy sa rozhodli "+str(q+1) for q in xrange(7)]
    legend+=["metoda1","best"]+["atribut "+str(q+1) for q in xrange(16)]+["dom "+str(q+1) for q in xrange(4)]+["hra","pocet dobrych","pocet zlych","poznamky"] 
    legend+=["metoda2","best"]+["stribut "+str(q+1) for q in xrange(16)]+["dom "+str(q+1) for q in xrange(4)]+["hra","pocet dobrych","pocet zlych","poznamky"] 
    for i,x in enumerate(legend):
        xl_met.write(0,i,x)
    
    for x in datadict:
        print str(datadict[x])
    for i,x in enumerate(usery):
        wanawrite = list(x[:3])
        print 
        print "sss"
        fix =[];
        if(x[3] == None):
            fix = [[1,1,0,0,0,0,1],"",["" for ww in xrange(4+7)]]
        else: demografia = json.loads(x[3])
        
        for w in sorted(demografia):
            fix.append(demografia[w])
        
        wanawrite += fix[2]     #mepovinne
        wanawrite += [fix[1]]      #kedy
        wanawrite += map(lambda ako: {0:'nie',1:'ano'}[ako], fix[0]) #ako
        
        x= x[1:]  #sprosta demografia mi to pokazila #TODO: ak ma len druhu metodu
        if(x[6] != None):
            data1 = datadict[x[6]]
            baad = sum([len(tmp[1]) for tmp in data1['aktivita'] ])
            wanawrite += [x[3]]+[data1['best_byt']]+padding(data1['atrib'],16)+data1['byty']+[data1['aktivita']]+[len(data1['aktivita']),baad, data1['poznamky']]
            if(x[7]!=None):
                data2 = datadict[x[7]]
                baad = sum([len(tmp[1]) for tmp in data2['aktivita'] ])
                wanawrite += [x[4],data2['best_byt']]+padding(data2['atrib'],16)+data2['byty']+[data2['aktivita']]+[len(data2['aktivita']),baad, data2['poznamky']]
        for j,co in enumerate(wanawrite):
            if( type(co) is int):
                xl_met.write(i+1,j,str(co))
            else:
                xl_met.write(i+1,j,unicode(co))
                pass
        
    
    wb.save('vysledky/vysledky.xls')
    return "Vysledky boli zgenerovane"


@app.route('/download123sav123psychologia')
def download(): # zmaz info o terajsej session
    
    return send_file("vysledky/vysledky.xls",
                     attachment_filename="vysledky.xls",
                     as_attachment=True);

## set the secret key.  keep this really secret:
app.secret_key = 'Zedol 666 metrov VELKY pes tento nahnity banan???'
  
if __name__ == '__main__':
  init_database()
  app.debug = True
  app.run(host='0.0.0.0')
