from elasticsearch import RequestError

import src
from src import server
from src.initialization import start_index


# Create if not exist
from src.server import app

try:
    start_index.create_index()
except RequestError:
    print("created not")
    pass


start_index.index()
app.run(debug=True, host='0.0.0.0')
