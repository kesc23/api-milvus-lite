from env import environment
from flask import Flask
from pymilvus import MilvusClient
from werkzeug.middleware.proxy_fix import ProxyFix

client = MilvusClient("./data/milvus.db")

server = Flask(__name__)

if environment["ENV_PRODUCTION"] == "true":
    server.wsgi_app = ProxyFix( server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1 )