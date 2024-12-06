from env import environment
from flask import request
from server import server as app
from routes.collection import *
from routes.vectors import *


if __name__ == "__main__":   
    import hypercorn.asyncio
    import asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:19530"]
    config.alpn_protocols = ["h2"]

    try:
        app.start_milvus()
        asyncio.run(hypercorn.asyncio.serve(app, config))
    finally:
        app.close_milvus()