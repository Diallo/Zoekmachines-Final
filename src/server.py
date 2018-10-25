# TODO: This gets done multiple times
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, RequestError

app = Flask(__name__)
app.elasticsearch = Elasticsearch(["http://localhost:9200"])

from src.initialization import start_index

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/res')
def result():
    return render_template('result.html')




