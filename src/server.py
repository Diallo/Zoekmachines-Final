# TODO: This gets done multiple times



    return decorated_function

from functools import wraps
import ast
import json
from collections import defaultdict, Counter

from flask import Flask, render_template, request, session
from elasticsearch import Elasticsearch, RequestError

from config import DEFAULT_DATA_PATH
from src.wordclouds import create_cloud

app = Flask(__name__)
app.elasticsearch = Elasticsearch(["http://localhost:9200"])


from src.search.functions import search_all,search_multiple
from src.initialization import start_index

from src.models.ted_talk import TedTalk
from datetime import datetime


def login_required(f):
    """ Function decorator assumes character name is set on login and unset on logout"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('password') is None:
            return "No login"
        return f(*args, **kwargs)



@app.route("/logmein")
def login_me():
    session['password'] = "good"



@app.route("/mult_search")
@login_required
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


    """
    
    <input class="field" type="text" placeholder="Search Term" name="search_term"/>

                <input class="field" type="text" placeholder="name_of_talk" name="name_of_talk"/>
                <input class="field" type="text" placeholder="speaker_name" name="speaker_name"/>
                <input class="field" type="text" placeholder="speaker_occupation" name="speaker_occupation"/>
                <input class="field" type="text" placeholder="event" name="event"/>
                <input class="field" type="text" placeholder="tags" name="tags"/>
                <input class="field" type="number" placeholder="min_views" name="min_views"/>
                <input class="field" type="number" placeholder="max_views" name="max_views"/>
                <input class="field" type="date" placeholder="min_date" name="min_date"/>
                <input class="field" type="date" placeholder="max_date" name="max_date"/>
                <input class="field" type="number" placeholder="min_duration(minutes)" name="min_duration"/>
                <input class="field" type="number" placeholder="max_duration(minutes)" name="max_duration"/>

                <input class="nbut" type="submit" value="Search"/>
                
    """




    fields = []
    #TODO search term
    # TODO SHOW USER QUERY USED
    # TODO format fields


    name_of_talk = request.args.get('name_of_talk').strip()
    if name_of_talk is not None and name_of_talk != "":
        fields.append({'name': name_of_talk})

    speaker_name = request.args.get('speaker_name').strip()
    if speaker_name is not None and speaker_name != "":
        fields.append({'main_speaker': speaker_name})

    speaker_occupation = request.args.get('speaker_occupation').strip()
    if speaker_occupation is not None and speaker_occupation != "":
        fields.append({'speaker_occupation': speaker_occupation})


    event = request.args.get('event').strip()
    if event is not None and event != "":
        fields.append({'event': event})

    tags = request.args.get('tags').strip()
    if tags is not None and tags != "":
        fields.append({'tags': tags.split(",")})


    min_views = request.args.get('min_views').strip()
    max_views = request.args.get('max_views').strip()
    if min_views is None or min_views == "":
        min_views = 0
    if max_views is None or max_views == "":
        max_views=500000000
    fields.append({'views': {"min": int(min_views), "max": int(max_views)}})



    min_duration =request.args.get('min_duration').strip()
    max_duration = request.args.get('max_duration').strip()
    if min_duration is None or min_duration == "":
        min_duration = 0
    if max_duration is None or max_duration == "":
        max_duration = 500000
    fields.append({'duration': {"min": int(min_duration)*60, "max": int(max_duration)*60}})



    min_date = request.args.get('min_date').strip()
    max_date = request.args.get('max_date').strip()
    if min_date is None or min_date == "":
        min_date = 0
    else:
        min_date = datetime.strptime(min_date, '%Y-%m-%d').strftime("%s")

    if max_date is None or max_date == "":
        max_date = datetime.now().strftime("%s")
    else:
        max_date = datetime.strptime(max_date, '%Y-%m-%d').strftime("%s")
    fields.append({'film_date': {"min": 	min_date, "max": 	max_date}}) # Unix timestamp



    term = request.args.get('search_term').strip()
    if term is not None and term != "":
        fields.append({'term': term})

    transcript = request.args.get("search_transcript") == "True"
    res,query = search_multiple(fields,transcript)
    r_str = ""
    for t_id in res:
        talk = TedTalk(t_id)
        r_str += talk.res_el()
    return render_template('result.html', r=r_str,query=query)



@app.route("/statistics")
@login_required
def show_statistics():
    tags = defaultdict(int)
    year = defaultdict(int)
    event = defaultdict(int)
    durations = []
    languages = []
    views = []


    with open(DEFAULT_DATA_PATH, 'r') as file:
        data = json.load(file)

        for talk in data:
            list_tags = ast.literal_eval(talk['tags']) # This bad

            for tag in list_tags:

                tags[tag] += 1


            # year["{}-01-01".format(datetime.fromtimestamp(int(talk['film_date'])).year)] += 1
            year[datetime.fromtimestamp(int(talk['film_date'])).year] += 1
            event[talk['event']] += 1
            durations.append(int(talk['duration']))
            languages.append(int(talk['languages']))
            views.append(int(talk['views']))

    yearkeys = sorted(year)

    print(len(durations))
    print(len(languages))
    print(len(views))
    print(len(event))
    print(len(year))
    print(len(tags))
    return render_template('statistics.html', **locals())
    
    
    


@app.route("/statistics1")
@login_required
def show_statistics1():
    tags = defaultdict(int)
    year = defaultdict(int)
    event = defaultdict(int)
    durations = []
    languages = []
    views = []


    with open(DEFAULT_DATA_PATH, 'r') as file:
        data = json.load(file)

        for talk in data:
            list_tags = ast.literal_eval(talk['tags']) # This bad

            for tag in list_tags:

                tags[tag] += 1


            # year["{}-01-01".format(datetime.fromtimestamp(int(talk['film_date'])).year)] += 1
            year[datetime.fromtimestamp(int(talk['film_date'])).year] += 1
            event[talk['event']] += 1
            durations.append(int(talk['duration']))
            languages.append(int(talk['languages']))
            views.append(int(talk['views']))

    yearkeys = sorted(year)
    
    
    duration = sum(durations)/len(durations) 
    languages = sum(languages)/len(languages)
    views = sum(views)/len(views)
 
    print(len(event))
    print(len(year))
    print(len(tags))
    return render_template('statistics1.html', **locals())
    
    

@app.route("/statistics2")
@login_required
def show_statistics2():
    tags = defaultdict(int)
    year = defaultdict(int)
    event = defaultdict(int)
    durations = []
    languages = []
    views = []


    with open(DEFAULT_DATA_PATH, 'r') as file:
        data = json.load(file)

        for talk in data:
            list_tags = ast.literal_eval(talk['tags']) # This bad

            for tag in list_tags:

                tags[tag] += 1


            # year["{}-01-01".format(datetime.fromtimestamp(int(talk['film_date'])).year)] += 1
            year[datetime.fromtimestamp(int(talk['film_date'])).year] += 1
            event[talk['event']] += 1
            durations.append(int(talk['duration']))
            languages.append(int(talk['languages']))
            views.append(int(talk['views']))

    yearkeys = sorted(year)

    print(len(durations))
    print(len(languages))
    print(len(views))
    print(len(event))
    print(len(year))
    print(len(tags))
    return render_template('statistics2.html', **locals())
    
    
@app.route("/statistics3")
@login_required
def show_statistics3():
    tags = defaultdict(int)
    year = defaultdict(int)
    event = defaultdict(int)
    durations = []
    languages = []
    views = []


    with open(DEFAULT_DATA_PATH, 'r') as file:
        data = json.load(file)

        for talk in data:
            list_tags = ast.literal_eval(talk['tags']) # This bad

            for tag in list_tags:

                tags[tag] += 1


            # year["{}-01-01".format(datetime.fromtimestamp(int(talk['film_date'])).year)] += 1
            year[datetime.fromtimestamp(int(talk['film_date'])).year] += 1
            event[talk['event']] += 1
            durations.append(int(talk['duration']))
            languages.append(int(talk['languages']))
            views.append(int(talk['views']))

    yearkeys = sorted(year)

    print(len(durations))
    print(len(languages))
    print(len(views))
    print(len(event))
    print(len(year))
    print(len(tags))
    return render_template('statistics3.html', **locals())


@app.route("/create_index")
@login_required
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
@login_required
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
@login_required
def static_file(path):
    return app.send_static_file(path)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/search')
@login_required
def search():
    return render_template('search.html')


@app.route('/res')
@login_required
def result():
    q = request.args.get('q')
    transcript = request.args.get("search_transcript") == "True"


    res,query = search_all(q,transcript)
    r_str = ""
    for t_id in res:
        talk = TedTalk(t_id)
        r_str += talk.res_el()
    return render_template('result.html', r=r_str,query=query)
    
    
@app.route('/wordcloud')
@login_required
def wordcloud():
    q = request.args.get('q')
    return render_template('wordcloud.html')
    

@app.route('/talk/<int:talk_id>')
@login_required
def talk(talk_id):
    try:
        t = TedTalk(talk_id, True)
    except ValueError as e:
        return str(e)

    create_cloud(talk_id,t.transcript)
    return render_template('talk.html', talk=t)




