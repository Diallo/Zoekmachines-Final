# TODO: This gets done multiple times
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, RequestError

app = Flask(__name__)
app.elasticsearch = Elasticsearch(["http://localhost:9200"])

from src.initialization import start_index

from src.models.ted_talk import TedTalk


@app.route("/create_index")
def create_index():
    """

    :return:
    """
    try:
        start_index.create_index()
        return "index created"
    except RequestError:
        return "already have index"

@app.route("/start_indexing")
def start_indexing():
    """

    :return:
    """
    if app.elasticsearch.count('testdata').get('count') > 1000:
        return "Already indexed"
    else:
        start_index.index()
        return "Indexing done"


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/res')
def result():
    return render_template('result.html')
    

@app.route('/talk/<int:talk_id>')
def talk(talk_id):
    try:
        t = TedTalk(talk_id, True)
    except ValueError as e:
        return str(e)
    return render_template('talk.html', talk=t)




