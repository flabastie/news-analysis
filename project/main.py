# main.py
# coding: utf-8

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, session, Response, redirect, request, url_for, jsonify
import json
import os.path
import random
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
from io import BytesIO  
# from io import StringIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
from project.processing.modeling import TopicsModelingLDA
from project.processing.modeling import TopicsModelingNMF
from project.queries.selection import SelectionAnalytics
import flask_monitoringdashboard as dashboard
from project import config

main = Blueprint('main', __name__)

@main.route('/')
def index():
    '''
        Page 'Cover'
        :param: None
        :return: render_template('index.html')
    '''
    return render_template('index.html')

@main.route('/home')
@login_required
def home():
    '''
        Page 'Home'
        :param url: url
        :type ur: str
        :return: render_template('home.html')
        :rtype: html page
    '''
    return render_template('home.html')

@main.route('/modeling')
@login_required
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
    # select sections lists
    selection_obj = SelectionAnalytics()
    sections_list = selection_obj.get_elements_list("section")
    # random key for select form
    random_item_key = random.choice(sections_list[:8])['key']
    return render_template("modeling.html", sections=sections_list, random_key=random_item_key)

@main.route("/topics", methods=['POST'])
@login_required
def topics():
    '''
        Corpus creation & making topic modeling
        :param '/topics': url
        :type '/topics': str
        :return: jsonify({'topics': topics})
        :rtype: json object
    '''
    if request.method == "POST":
        req = request.form.to_dict()
        params = {
            "sel_twords" : int(req['sel_twords']),
            "sel_model" : req['sel_model'],
            "sel_section" : req['sel_section'],
            "sel_topics" : int(req['sel_topics']),
            "sel_docs" : int(req['sel_docs'])
        }
        if (req and params['sel_model']=='LDA') :
            selection_obj = SelectionAnalytics()
            # custom corpus
            corpus = selection_obj.get_custom_corpus_list(params["sel_section"], params["sel_docs"])
            # model obj
            model_obj = TopicsModelingLDA(params["sel_twords"], params["sel_topics"], corpus)
            # data fit
            data_fitted = model_obj.fit_data()
            # get topics
            topics = model_obj.get_topics()
            # set session variable topics_params
            session['topics_params'] = params
            return jsonify({'topics': topics})

        elif (req and params['sel_model']=='NMF') :
            selection_obj = SelectionAnalytics()
            # custom corpus
            corpus = selection_obj.get_custom_corpus_list(params["sel_section"], params["sel_docs"])
            # model obj
            model_obj = TopicsModelingNMF(params["sel_twords"], params["sel_topics"], corpus)
            # data fit
            data_fitted = model_obj.fit_data()
            # get topics
            topics = model_obj.get_topics()
            # set session variable topics_params
            session['topics_params'] = params
            return jsonify({'topics': topics})

        else:
            return jsonify({'topics': None})

@main.route("/search", methods=['POST'])
@login_required
def search():
    '''
        Get words selected,
        set session variable tokens_search
        & resend to ajax to redirect
        :param '/search': url
        :type '/search': str
        :return: jsonify({'result': 1})
        :rtype: json object
    '''
    if request.method == "POST":
        req = request.form.to_dict()
        words = req['w']
        print(words)
        if req and len(words) > 0:
            # set session variable tokens_search
            session['tokens_search'] = words.split(",")
            return jsonify({'result': 1})
        else:
            return jsonify({'result': 0})

@main.route("/exploration")
@login_required
def exploration():
    '''
        Get tokens_search from session
        & return exploration template
        (List of documents links)
        :param '/exploration': url
        :type '/exploration': str
        :return: data, hits, wanted, docs
        :rtype: list, int, int, list
        :return: render_template('home.html')
        :rtype: html page
    '''
    # get tokens_search from session
    if 'tokens_search' in session:
        # tokens_search = session['tokens_search']
        # return render_template("exploration.html", data=tokens_search)
        tokens_search = ','.join(session['tokens_search'])
        selection_obj = SelectionAnalytics()
        nb_docs = 50
        res = selection_obj.get_documents(tokens_search, nb_docs)
        # print(res)
        return render_template("exploration.html", data=tokens_search, hits=res[0], wanted=res[1], docs=res[2])
    else:
        return "null"

@main.route('/document/<string:id>', methods=['GET'])
@login_required
def document(id):
    '''
        Get doc id
        & return doc data & id
        :param '/document/<string:id>': url + doc id
        :type '/document/<string:id>': str
        :return: data, id
        :rtype: dict, str
        :return: render_template("document.html")
        :rtype: html page
    '''
    if id:
        selection_obj = SelectionAnalytics()
        res = selection_obj.get_document_by_id(id)
        return render_template("document.html", data=res['_source'], id=id)
    else:
        return "ERROR"

@main.route('/statistics/<string:id>', methods=['GET'])
@login_required
def statistics(id):
    '''
        Get doc id
        & return doc data & id
        :param '/statistics/<string:id>': url + doc id
        :type '/statistics/<string:id>': str
        :return: data, id
        :rtype: dict, str
        :return: render_template("statistics.html")
        :rtype: html page
    '''
    if id:
        # get document by id
        selection_obj = SelectionAnalytics()
        res = selection_obj.get_document_by_id(id)
        # return statistics.html
        return render_template("statistics.html", data=res['_source'], id=id)
    else:
        return "ERROR"

@main.route('/wordcloud/<string:id>', methods=['GET'])
@login_required
def wordcloud_png(id):
    '''
        Get doc id
        & return wordcloud image from
        :param '/wordcloud/<string:id>': url + doc id
        :type '/wordcloud/<string:id>': str
        :return: Response(img, mimetype='image/png')
        :rtype: img object
    '''
    # get document by id
    selection_obj = SelectionAnalytics()
    res = selection_obj.get_document_by_id(id)
    tokens_list = res['_source']['doc_token']
    # create wordcloud
    text_wordcloud =  ' '.join(tokens_list) 
    wordcloud = WordCloud(max_font_size=50, max_words=100, width=800, height=600, margin=0, background_color="white").generate(text_wordcloud)
    # save wordcloud image
    img = BytesIO()
    wordcloud.to_image().save(img, 'PNG')
    img.seek(0)
    # return wordcloud image
    return Response(img, mimetype='image/png')

@main.route('/barplot/<string:id>', methods=['GET'])
@login_required
def barplot(id):
    '''
        Get doc id
        & return barplot image from
        :param '/barplot/<string:id>': url + doc id
        :type '/barplot/<string:id>': str
        :return: Response(img, mimetype='image/png')
        :rtype: img object
    '''
    # get document by id
    selection_obj = SelectionAnalytics()
    res = selection_obj.get_document_by_id(id)
    tokens_list = res['_source']['doc_token']
    # data
    counter = Counter()
    counter.update(tokens_list)
    most_common = counter.most_common(25)
    df = pd.DataFrame(most_common, columns=['token', 'score'])
    scores = df['score']
    words = df['token']
    # figure
    fig = Figure(figsize=(8, 8))
    y_pos = np.arange(len(words))
    ax = fig.add_subplot(111)
    ax.barh(y_pos, scores, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Scores')
    ax.set_title('Words frequencies')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    # return barplot image
    return Response(output.getvalue(), mimetype='image/png')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)