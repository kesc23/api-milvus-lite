from env import environment
from server import server as app
from routes.collection import *

app.run(port=19530, debug=(environment["DEBUG"] == "true"), host="0.0.0.0")