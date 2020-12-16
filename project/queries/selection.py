from elasticsearch import Elasticsearch, exceptions
import json, time
import itertools
from project import config

class SelectionAnalytics():
    '''
        SelectionAnalytics class
        data analytics - elasticsearch
    '''
    # declare globals for the Elasticsearch client host
    DOMAIN = config.DOMAIN
    LOGIN = config.LOGIN
    PASSWORD = config.PASSWORD
    PORT = config.PORT
    index_name = 'news_analysis'
    client = None

    def __init__(self):
        '''
            Create an Elasticsearch connection object
            :param index_name: index name
            :type index_name: string
            :return: null
        '''
        self.client = Elasticsearch( [self.DOMAIN],
                            http_auth=(self.LOGIN, self.PASSWORD),
                            scheme="https", 
                            port=self.PORT)
        # Confirming there is a valid connection to Elasticsearch
        try:
            # use the JSON library's dump() method for indentation
            info = json.dumps(self.client.info(), indent=4)
            # pass client object to info() method
            print ("Elasticsearch client info():", info)
        except exceptions.ConnectionError as err:
            # print ConnectionError for Elasticsearch
            print ("\nElasticsearch info() ERROR:", err)
            print ("\nThe client host:", host, "is invalid or cluster is not running")
            # change the client's value to 'None' if ConnectionError
            self.client = None

    def get_elements_list(self, element_name):
        '''
            get_elements_list
            :param self: self
            :type self: None
            :param element_name: element_name
            :type element_name: str
            :return: elements_list
            :rtype: list of dics (doc_count & key)
        '''
        res = self.client.search(index=self.index_name, body={
                "size": 0,
                "aggs": {
                    "Articles": {
                        "filter": {
                            "range": {
                                "date": {
                                    "gte": "2020-01-01T00:00:00.00"
                                }
                            }
                        },
                        "aggs": {
                            "GroupBy": {
                                "terms": { "field": element_name + ".keyword", "size": 10000 } 
                            }
                        }
                    }
                }
            }
        )
        elements_docs = res['aggregations']['Articles']['GroupBy']['buckets']
        # sorting by doc_count desc
        elements_list  = [item for item in sorted(elements_docs, key = lambda i: i['doc_count'], reverse=True)]
        # list of dics (doc_count & key)
        return elements_list[:20]
    
    def get_custom_corpus(self, section_name, query_size):
        '''
            get_custom_corpus
            :param section_name: section_name
            :type section_name: str
            :param query_size: query_size
            :type query_size: int
            :return: (custom_corpus, total_hits)
            :rtype: dict (custom_corpus & total_hits)
        '''
        res = self.client.search(index=self.index_name, body= {
                "size": query_size,
                "query": {
                    # "match": {
                    #     "section": section_name
                    # }
                    "bool" : {
                        "must" : {
                            "term" : { "section" : section_name }
                        },
                    },
                },
                "_source": ["doc_token"]
            }
        )
        # total hits
        total_hits = res['hits']['total']['value']
        # concat doc_token fields from documents
        results_list = []
        results_list = [item["_source"]['doc_token'] for item in res['hits']['hits']]
        # merge lists to unique list of tokens
        custom_corpus = list(itertools.chain.from_iterable(results_list))
        return (custom_corpus, total_hits)

    def get_documents(self, string_search, nb_wanted):
        '''
            get_documents
            :param string_search: tokens to search
            :type string_search: str
            :param nb_wanted: total docs wanted
            :type nb_wanted: int
            :return: (hits, nb_wanted, documents_list)
            :rtype: tuple
        '''
        res = self.client.search(index=self.index_name, body={
                "size": nb_wanted,
                "query": {
                    "match": {
                        "doc_token": string_search 
                    },
                },
                "_source": {
                    "include": ["author", "date", "link", "section", "title"]
                },
            }
        )
        hits = res['hits']['total']['value']
        documents_list = res['hits']['hits']
        return (hits, nb_wanted, documents_list)

    def get_document_by_id(self, id_doc):
        '''
            get_documents
            :param id_doc: id_doc
            :type id_doc: str
            :return: doc
            :rtype: dict
        '''
        res = self.client.search(index=self.index_name, body={
                "size": 1,
                "query": {
                    "terms": {
                    "_id": [id_doc] 
                    },
                },
                "_source": {
                    "include": ["author", "content_html", "date", "doc_token", "link", "teaser", "section", "title"]
                },
            }
        )
        doc = res['hits']['hits'][0]
        return doc

    def get_custom_corpus_list(self, section_name, query_size):
        '''
            get_custom_corpus
            :param section_name: section_name
            :type section_name: str
            :param query_size: query_size
            :type query_size: int
            :return: custom_corpus
            :rtype: list of lists
        '''
        res = self.client.search(index='news_analysis', body= {
                "size": query_size,
                "query": {
                    "bool" : {
                        "must" : {
                            "term" : { "section" : section_name }
                        },
                    },
                },
                "_source": ["doc_token"]
            }
        )
        # from doc_token fields create list of lists
        results_list = []
        results_list = [item["_source"]['doc_token'] for item in res['hits']['hits']]
        return (results_list)

class SelectionRelational():
    '''
        SelectionRelational class
        data statistics - Azure SQL
    '''
    def __init__(self):
        '''
            Create an Elasticsearch connection object
            :param index_name: index name
            :type index_name: string
            :return: null
        '''
        return 'hello SelectionRelational'