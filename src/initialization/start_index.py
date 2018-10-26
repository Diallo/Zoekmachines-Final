"""
Called upon starting the search engine to index all the required data.
"""
import json

import config
from src.server import app
from elasticsearch import helpers

def create_index():

    body = {

        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },

        'mappings': {
            'generated': {

                "properties": {

                    "comments": {"type": "integer"},
                    "description": {"type": "text"},
                    "duration": {"type": "integer"},
                    "event": {"type": "text"},
                    "film_date": {"type": "date",
                                  },
                    "languages": {"type": "integer"},
                    "main_speaker": {"type": "text"},
                    "name": {"type": "text"},
                    "num_speaker": {"type": "integer"},
                    "published_date": {
                        "type": "date",

                    },
                    "ratings": {"type": "text"},
                    "related_talks": {"type": "text"},
                    "speaker_occupation": {"type": "text"},
                    "tags": {"type": "text"},
                    "title": {"type": "text"},
                    "transcript": {"type": "text"},
                    "url": {"type": "text"},
                    "views": {"type": "integer"}
                }
            }
        }

    }


    app.elasticsearch.indices.create(
        index="testdata",
        body=body
    )

def index(data=config.DEFAULT_DATA_PATH):
    """Index all the data

    :return:
    """
    with open(data) as raw_data:
        json_docs = json.load(raw_data)
        helpers.bulk(app.elasticsearch, json_docs, index='testdata', doc_type='generated')

