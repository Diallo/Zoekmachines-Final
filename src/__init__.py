from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/search')
def search():
    return render_template('search.html')
    
    
@app.route('/res')
def result():
    return render_template('result.html')


app.run(debug=True, host='0.0.0.0')
