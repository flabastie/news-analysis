import pytest
from project import main

def index():
    response = app.test_client().get('/')
    assert response.status_code == 200

def home():
    response = app.test_client().get('/')
    assert response.status_code == 200

def modeling():
    '''
        Page 'Modeling'
        :param '/modeling': url
        :type ur: str
        :return: sections, random_key
        :rtype: list, str
        :return: render_template('home.html')
        :rtype: html page
    '''
    response = app.test_client().get('/')
    assert response.status_code == 200
    # select sections lists
    selection_obj = SelectionAnalytics()
    # test result of function SelectionAnalytics is object
    assert isinstance(selection_obj, obj) == True
    # get_elements_list("international")
    sections_list = selection_obj.get_elements_list("international")
    # test result of get_elements_list is list
    assert isinstance(sections_list, list) == True
    # random key for select form
    random_item_key = random.choice(sections_list[:8])['key']
    # test result of random.choice is string
    assert isinstance(random_item_key, str) == True


def topics():
    '''
        Corpus creation & making topic modeling
        :param '/topics': url
        :type '/topics': str
        :return: jsonify({'topics': topics})
        :rtype: json object
    '''
    response = app.test_client().get('/')
    assert response.status_code == 200

    # test request.method
    assert request.method == "POST"

    # test request.form.to_dict()
    req = request.form.to_dict()
    assert isinstance(req, dict) == True

    # test params received
    params = {
            "sel_twords" : int(8),
            "sel_model" : 'nmf',
            "sel_section" : 'international',
            "sel_topics" : 5,
            "sel_docs" : 100
        }


    selection_obj = SelectionAnalytics()
    #         # custom corpus
    #         corpus = selection_obj.get_custom_corpus_list(params["sel_section"], params["sel_docs"])
    #         # model obj
    #         model_obj = TopicsModelingLDA(params["sel_twords"], params["sel_topics"], corpus)
    #         # data fit
    #         data_fitted = model_obj.fit_data()
    #         # get topics
    #         topics = model_obj.get_topics()
    #         # set session variable topics_params
    #         session['topics_params'] = params
    #         return jsonify({'topics': topics})
    #     elif (req and params['sel_model']=='NMF') :
    #         selection_obj = SelectionAnalytics()
    #         # custom corpus
    #         corpus = selection_obj.get_custom_corpus_list(params["sel_section"], params["sel_docs"])
    #         # model obj
    #         model_obj = TopicsModelingNMF(params["sel_twords"], params["sel_topics"], corpus)
    #         # data fit
    #         data_fitted = model_obj.fit_data()
    #         # get topics
    #         topics = model_obj.get_topics()
    #         # set session variable topics_params
    #         session['topics_params'] = params
    #         return jsonify({'topics': topics})
    #     else:
    #         return jsonify({'topics': None})

def search():
    response = app.test_client().get('/')
    assert response.status_code == 200

def exploration():
    response = app.test_client().get('/')
    assert response.status_code == 200

def document(id):
    response = app.test_client().get('/')
    assert response.status_code == 200

def statistics(id):
    response = app.test_client().get('/')
    assert response.status_code == 200

def wordcloud_png(id):
    response = app.test_client().get('/')
    assert response.status_code == 200

def barplot(id):
    response = app.test_client().get('/')
    assert response.status_code == 200