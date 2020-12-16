import pytest
# import sys 
# import os
from queries.selection import SelectionAnalytics

def test_get_elements_list():
    '''
        test get_elements_list
        :param element_name: element_name
        :type element_name: str
        :return: elements_list
        :rtype: list of dics (doc_count & key)
    '''
    # param get_elements_list()
    param = 'section'
    # SelectionAnalytics instance
    process_doc = SelectionAnalytics()
    # use function get_elements_list()
    result_get_elements_list = process_doc.get_elements_list(param)
    # test result of function get_elements_list is list
    assert isinstance(result_get_elements_list, list) == True
    # test elements result are dict
    assert isinstance(result_get_elements_list[0], dict) == True
    # test 1st elements of dict is int
    assert isinstance(result_get_elements_list[0]['doc_count'], int) == True
    # test 2nd elements of dict is string
    assert isinstance(result_get_elements_list[0]['key'], str) == True

def test_get_custom_corpus():
    '''
        test get_custom_corpus
        :param section_name: section_name
        :type section_name: str
        :param query_size: query_size
        :type query_size: int
        :return: (custom_corpus, total_hits)
        :rtype: tuple (custom_corpus, total_hits)
    '''
    # params get_custom_corpus()
    param_section_name = 'emploi'
    param_query_size = '10'
    # SelectionAnalytics instance
    process_doc = SelectionAnalytics()
    # use function get_custom_corpus()
    corpus = process_doc.get_custom_corpus(param_section_name, param_query_size)
    # test result of function get_custom_corpus is tuple
    assert isinstance(corpus, tuple) == True
    # test corpus[0] is list
    assert isinstance(corpus[0], list) == True
    # test corpus[1] is int
    assert isinstance(corpus[1], int) == True