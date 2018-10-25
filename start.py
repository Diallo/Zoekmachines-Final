from elasticsearch import RequestError


from src.initialization import start_index


# Create if not exist
from src.server import app





app.run(debug=True, host='0.0.0.0')
