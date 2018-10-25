from flask import Flask, render_template, request
import src.py.talk


app = Flask(__name__)


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    return render_template('index.html')
  
    
@app.route('/res')
def result():
    return render_template('result.html')
    
    
@app.route('/talk/<int:talk_id>')
def talk(talk_id):
    return render_template('talk.html', t_id=talk_id)


app.run(debug=True, host='0.0.0.0')
