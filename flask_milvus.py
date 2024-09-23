from os import environ
from pymilvus import MilvusClient
from flask import Flask

class Server(Flask):

    def __init__(self, data):
        super().__init__(data)
        self.milvus = None
        if environ.get('WERKZEUG_RUN_MAIN') == 'true':
            self.start_milvus()

    def start_milvus(self):
        if not self.milvus:
            self.milvus = MilvusClient("./data/milvus.db")

    def close_milvus(self):
        if self.milvus:
            self.milvus.close()
            self.milvus = None

    def __del__(self):
        self.close_milvus()
        