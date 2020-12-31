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
        # remove empty sections (bug to fix)
        sections_to_exclude = ['les-decodeurs', 'm-le-mag', 'm-perso', 'm-styles', 'series-d-ete']
        for item in elements_list[:18]:
            # print(item)
            if (item['key'] in sections_to_exclude):
                elements_list.remove(item)
        # list of dics (doc_count & key)
        return elements_list[:18]
    
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

    def count_by_sections(self):
        '''
            count docs by sections
            :return: sections_list
            :rtype: list of dicts
        '''
        res = self.client.search(index='news_analysis', body={
                # "size": 9999,
                "aggs": {
                    "sections": {
                    "terms": { "field": "section.keyword" } 
                    }
                },
                "_source": {
                    "include": ["_id", "date", "section"]
                },
            }
        )
        result = res['aggregations']['sections']
        buckets = result['buckets'][:9]
        sections_list = []
        # get total docs 
        total_docs = 0
        for item in buckets:
            total_docs += item['doc_count']
        # get percent
        for item in buckets:
            doc_percent = round(item['doc_count']/total_docs*100)
            sections_list.append({'score':item['doc_count'], 'percent':doc_percent, 'section':item['key']})

        # Rename sections
        sections_names = {
            'international': 'International',
            'economie':'Economie',
            'planete': 'Planète',
            'idees':'Idées',
            'afrique':'Afrique',
            'politique':'Politique',
            'societe': 'Societe',
            'culture':'Culture',
            'sport':'Sport'
        }
        for item in sections_list:
            if item['section'] in sections_names:
                item['section']= sections_names[item['section']]

        return(sections_list)

    def count_by_dates(self):
        res = self.client.search(index='news_analysis', body={
            "aggs": {
                "amount_per_week": {
                "date_histogram": {
                    "field": "date",
                    "interval": "week",
                    "format" : "yyyy-MM-dd"
                },
                # "aggs": {
                #     "total_amount": {
                #     "sum": {
                #         "field": "date"
                #     }
                #     }
                # },
                "aggs": {
                    "sections": {
                        "terms": { "field": "section.keyword" } 
                    }
                },
                }
            },
            }
        )
        res_list = res['aggregations']['amount_per_week']['buckets']

        # dict for sections selection & renaming
        sections_names = {
            'international': 'International',
            'economie':'Economie',
            'planete': 'Planète',
            'idees':'Idées',
            'afrique':'Afrique',
            'politique':'Politique',
            'societe': 'Société',
            'culture':'Culture',
            'sport':'Sport'
        }

        # build data list
        data = []
        for item in res_list:
            nb_docs = item['doc_count']
            # filter year 2020
            year = item['key_as_string'][0:4]
            if (year != '2019'):
                # get & subtring date
                date = item['key_as_string'][0:10]
                buckets = item['sections']['buckets']
                sections_scores = []
                # select sections and rename
                for i in buckets:
                    if i['key'] in sections_names:
                        sections_scores.append({'section':sections_names[i['key']], 'score':i['doc_count']})

                # set empty sections to zero
                listed_sections = [element['section'] for element in sections_scores]
                for name in sections_names.values():
                    if name not in listed_sections:
                        sections_scores.append({'section':name, 'score':0})

                # data list to return
                data.append({'date':date, 'nb_docs':nb_docs, 'sections_scores':sections_scores})

        # reformat data
        data_list = []
        for item in data:
            item_dict = {'date': item['date'].replace('-', '')}
            for element in item['sections_scores']:
                item_dict[element['section']] = element['score']
            data_list.append(item_dict)
        
        return data_list

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