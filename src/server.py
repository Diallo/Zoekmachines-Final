# TODO: This gets done multiple times
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, RequestError


app = Flask(__name__)
app.elasticsearch = Elasticsearch(["http://localhost:9200"])


from src.search.functions import search_all,search_multiple
from src.initialization import start_index

from src.models.ted_talk import TedTalk


@app.route("/searcher")
def searcher():
    return search_all("Downside Drug Dealer Being")

@app.route("/mult_search")
def  mult_search():
    """Search in multiple fields within ted talks


    Possibilities are:

    1.) searching by event (ted/x event)   X
    2.) Searching in duration range (minutes is passed converted to seconds)
    3.) Search in range of film date
    4.) Search by name of speaker (exact)    X
    5.) Search in Title (Name field     X
    6.) Search by speaker occupation   X
    7.) Search by views range    X
    8.) regular description search also
    9.) Search by a list of tags  X
    :return:
    """

    fields = []

    fields.append({'duration':{"min":1160,"max":1200}})
    fields.append({'event':'TED2006'})
    fields.append({'film_date': {"min": 	1140825500, "max": 	1140825900}}) # Unix timestamp
    fields.append({'main_speaker':'Ken Robinson'})
    fields.append({'name':"schools kill"})
    fields.append({'speaker_occupation':'Author'})
    fields.append({'tags':['children','creativity']})
    fields.append({'views': {"min": 5, "max": 47527110}})

    return search_multiple(fields)

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
    q = request.args.get('q')
    res = search_all(q)
    r_str = ""
    for t_id in res:
        talk = TedTalk(t_id)
        r_str += talk.res_el()
    return render_template('result.html', r=r_str)
    
    
@app.route('/wordcloud')
def wordcloud():
    q = request.args.get('q')
    return render_template('wordcloud.html')
    

@app.route('/talk/<int:talk_id>')
def talk(talk_id):
    try:
        t = TedTalk(talk_id, True)
    except ValueError as e:
        return str(e)
    return render_template('talk.html', talk=t)




