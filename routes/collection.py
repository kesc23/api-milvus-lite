from pymilvus import CollectionSchema, MilvusClient
from pymilvus.milvus_client import IndexParams
from operator import itemgetter
from flask import request
from server import server, client as milvus
from response import execute

def get_payload() -> dict: return request.json
