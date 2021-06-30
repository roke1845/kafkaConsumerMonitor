from elasticsearch import Elasticsearch


class ESConnection():
    def __init__(self, es_url_list, username, password):
        self.conn = Elasticsearch(es_url_list, http_auth=(username, password))

    def send(self, index_name, body, mapping=""):
        if not self.conn.indices.exists(index_name):
            self.conn.indices.create(index=index_name, body=mapping)

        self.conn.index(index=index_name, body=body)