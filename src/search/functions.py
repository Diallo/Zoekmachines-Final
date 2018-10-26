"""
Description
"""

from autocorrect import spell
from nltk.corpus import stopwords

from src.server import app


def search_multiple(fields,transcript):
    query = {"query":
        {
            "bool": {
                "must": [],
                "should": [],

            }
        }
    }

    # TODO: description and range
    query_used = {}
    for field in fields:
        query_field, query_value = next(iter(field.items()))



        if query_field == "term":

            query_value = query_value.lower().split()

            query_value = [word for word in query_value if word not in stopwords.words('english')]

            query_value = [spell(query_value) for query_value in query_value]
            query_value = " ".join(query_value)

            print(query_value)

            query['query']['bool']['should'].append({"match": {"description": query_value}})
            query['query']['bool']['should'].append({"match": {"title": query_value}})
            if transcript:
                query['query']['bool']['should'].append({"match": {"transcript": query_value}})


        if query_field == "event":
            query['query']['bool']['must'].append({"match": {"event": query_value}})

        if query_field == "main_speaker":
            query['query']['bool']['must'].append({"match": {"main_speaker": query_value}})
        if query_field == "name":
            query['query']['bool']['must'].append({"match": {"name": query_value}})

        if query_field == "speaker_occupation":
            query['query']['bool']['must'].append({"match": {"speaker_occupation": query_value}})
        if query_field == "tags":
            pass
        if query_field == "views":
            min_value = query_value['min']
            max_value = query_value['max']

            query['query']['bool']['must'].append({"range": {"views": {"gte": min_value, "lte": max_value}}})
        if query_field == "film_date":
            min_value = query_value['min']
            max_value = query_value['max']
            query['query']['bool']['must'].append({"range": {"film_date": {"gte": min_value, "lte": max_value}}})
        if query_field == "duration":
            min_value = query_value['min']
            max_value = query_value['max']
            query['query']['bool']['must'].append({"range": {"duration": {"gte": min_value, "lte": max_value}}})
        query_used[query_field] = query_value


    res = app.elasticsearch.search(index="testdata", doc_type="generated",

                                   body=query)

    print("%d documents found" % res['hits']['total'])
    print(res['hits']['max_score'])
    rdocs = []
    for doc in res['hits']['hits']:
        rdocs.append(int(doc['_id']))
    return rdocs,query_used


def search_all(term, transcript):
    term = term.lower().split()

    term = [word for word in term if word not in stopwords.words('english')]

    term = [spell(term) for term in term]
    term = " ".join(term)

    if transcript:
        query = {
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"description": term}},
                        {"match": {"event": term}},
                        {"match": {"main_speaker": term}},
                        {"match": {"name": term}},
                        {"match": {"speaker_occupation": term}},
                        {"match": {"tags": term}},
                        {"match": {"title": term}},
                        {"match": {"transcript": term}},
                    ],
                    "tie_breaker": 0.3
                }
            }
        }
    else:
        query = {"query": {
            "multi_match": {
                "query": term,
                "type": "most_fields",
                "fields": ["description", "event", "main_speaker", "name", "speaker_occupation", "tags", "title",
                           ]
            }
        }}

    res = app.elasticsearch.search(index="testdata", doc_type="generated",

                                   body=query)

    print("%d documents found" % res['hits']['total'])
    print(res['hits']['max_score'])
    rdocs = []
    for doc in res['hits']['hits']:
        rdocs.append(int(doc['_id']))

    return rdocs,term
