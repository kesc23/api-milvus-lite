from env import environment
from server import server as app
from routes.collection import *


if __name__ == "__main__":
    try:
        app.start_milvus()
        app.run(port=19530, host="0.0.0.0")
    finally:
        app.close_milvus()