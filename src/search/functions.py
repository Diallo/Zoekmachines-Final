"""
Description
"""
import json

from autocorrect import spell
from nltk.corpus import stopwords

from src.server import app


# def search_all(term):
#     res = app.elasticsearch.search(index="testdata", doc_type="generated",
#
#                                    body={
#                                        "query": {
#                                            "multi_match": {
#                                                "query": term,
#                                                "type": "most_fields",
#                                                "fields": ["description","event","main_speaker","name^50","speaker_occupation","tags","title^2","transcript"]
#                                            }
#                                        }
#                                    })
#
#     print("%d documents found" % res['hits']['total'])
#     print(res['hits']['max_score'])
#     for doc in res['hits']['hits']:
#         print("%s) %s" % (doc['_id'], doc['_source']['name']))
#         print("%s) %s" % (doc['_id'], doc['_source']['description']))
#         print(doc['_score'])
#         print("\n\n")
#
#     return "a"

def search_multiple(fields):
    query = {"query":
        {
            "bool": {
                "must": [],
                "should": [],


            }
        }
    }

    # TODO: description and range

    for field in fields:
        query_field, query_value = next(iter(field.items()))

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

            query['query']['bool']['must'].append(  {"range":{"views": {"gte": min_value, "lte": max_value}}})
        if query_field == "film_date":
            min_value = query_value['min']
            max_value = query_value['max']
            query['query']['bool']['must'].append(  {"range":{"film_date": {"gte": min_value, "lte": max_value}}})
        if query_field == "duration":
            min_value = query_value['min']
            max_value = query_value['max']
            query['query']['bool']['must'].append(  {"range":{"duration": {"gte": min_value, "lte": max_value}}})



    res = app.elasticsearch.search(index="testdata", doc_type="generated",

                                   body=query)

    print("%d documents found" % res['hits']['total'])
    print(res['hits']['max_score'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['name']))
        print("%s) %s" % (doc['_id'], doc['_source']['description']))
        print("%s) %s" % (doc['_id'], doc['_source']['main_speaker']))
        print("%s) %s" % (doc['_id'], doc['_source']['title']))
        print("%s) %s" % (doc['_id'], doc['_source']['url']))
        print(doc['_score'])
        print("\n\n")

    return "a"


def search_all(term):
    term = term.lower().split()

    term = [word for word in term if word not in stopwords.words('english')]

    term = [spell(term) for term in term]
    term = " ".join(term)

    print(term)

    res = app.elasticsearch.search(index="testdata", doc_type="generated",

                                   body={
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
                                   })

    print("%d documents found" % res['hits']['total'])
    print(res['hits']['max_score'])
    rdocs = []
    for doc in res['hits']['hits']:
        # print("%s) %s" % (doc['_id'], doc['_source']['name']))
        # print("%s) %s" % (doc['_id'], doc['_source']['description']))
        # print("%s) %s" % (doc['_id'], doc['_source']['main_speaker']))
        # print("%s) %s" % (doc['_id'], doc['_source']['title']))
        # print("%s) %s" % (doc['_id'], doc['_source']['url']))
        # print(doc['_score'])
        # print("\n\n")
        rdocs.append(int(doc['_id']))

    return rdocs
