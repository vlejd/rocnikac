from flask import Flask
execfile("lib.py")
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/ping')
def ping():
    s = pingg("http://people.ksp.sk/~vlejd/projekt.html")
    print s
    return s

if __name__ == '__main__':
    app.run(host='0.0.0.0')
