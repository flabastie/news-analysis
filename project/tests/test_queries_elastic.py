import pytest
from project.queries.selection import SelectionAnalytics

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

def test_get_custom_corpus_list():
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

def get_documents():
    '''
        get_documents
        :param string_search: tokens to search
        :type string_search: str
        :param nb_wanted: total docs wanted
        :type nb_wanted: int
        :return: (hits, nb_wanted, documents_list)
        :rtype: tuple
    '''
    # params get_documents()
    param_string_search = 'enseignants, écoles, éducation'
    param_nb_wanted = 10
    # SelectionAnalytics instance
    process_doc = SelectionAnalytics()
    # use function get_documents()
    res = selection_obj.get_documents(tokens_search, nb_docs)
    # test res is tuple
    assert isinstance(res, tuple)
    # test res[0] is int
    assert isinstance(res[0], int)
    # test res[1] is int
    assert isinstance(res[1], int)
    # test res[2] is list
    assert isinstance(res[2], list)

def get_document_by_id():
    '''
        get_documents
        :param id_doc: id_doc
        :type id_doc: str
        :return: doc
        :rtype: dict
    '''
    # params get_document_by_id()
    param_id_doc = 'YPETBXYBFL8Y9aYU1wrA'
    # use function get_document_by_id()
    selection_obj = SelectionAnalytics()
    res = selection_obj.get_document_by_id(id)
    # test res is dict
    assert isinstance(res, dict)