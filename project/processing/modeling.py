from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

class TopicsModelingLDA():

        n_topics = 3
        nb_top_words = 3
        tf_vectorizer = None
        tf = None
        lda = None

        def __init__(self, nb_top_words, n_topics, corpus):
                '''
                        Create LDA object
                        :param nb_top_words: number of top-words
                        :type nb_top_words: int
                        :param n_topics: number of topics
                        :type n_topics: int
                        :param corpus: data
                        :type corpus: list
                        :return: None
                '''
                # number of top-words
                self.nb_top_words = nb_top_words
                # number of topics
                self.n_topics = n_topics
                # vectorizer
                self.tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=500)
                self.tf = self.tf_vectorizer.fit_transform(corpus)
                # create LDA model
                self.lda = LatentDirichletAllocation(
                        n_components=n_topics, 
                        max_iter=5, 
                        learning_method='online', 
                        learning_offset=50.,
                        random_state=0)

        def fit_data(self):
                '''
                        fit_data
                        :param no_params: no params
                        :return lda.fit: lda fitted
                        :rtype: object
                '''
                # Fitter sur les données
                return self.lda.fit(self.tf)

        def get_topics(self):
                '''
                        get_topics
                        :param no_params: no params
                        :return topics_list: List of topics
                        :rtype: list of tuples
                '''
                feature_names = self.tf_vectorizer.get_feature_names()
                topics_list = []
                for topic_idx, topic in enumerate(self.lda.components_):
                        top_words_list = [feature_names[i] for i in topic.argsort()[:-self.nb_top_words - 1:-1]]
                        # top_words_string = " ".join(top_words_list)
                        item_tp = (topic_idx, top_words_list)
                        topics_list.append(item_tp)                        
                return topics_list


class TopicsModelingNMF():

        n_topics = 3
        nb_top_words = 3
        tfidf_vectorizer = None
        tfidf = None
        nmf = None

        def __init__(self, nb_top_words, n_topics, corpus):
                '''
                        Create LDA object
                        :param nb_top_words: number of top-words
                        :type nb_top_words: int
                        :param n_topics: number of topics
                        :type n_topics: int
                        :param corpus: data
                        :type corpus: list
                        :return: None
                '''
                # number of top-words
                self.nb_top_words = nb_top_words
                # number of topics
                self.n_topics = n_topics
                # vectorizer
                self.tfidf_vectorizer = TfidfVectorizer(analyzer='word', tokenizer=self.dummy_fun, preprocessor=self.dummy_fun, token_pattern=None)  
                self.tfidf = self.tfidf_vectorizer.fit_transform(corpus)
                # create NMF model
                self.nmf = NMF(n_components=n_topics, 
                                random_state=1, 
                                alpha=.1, 
                                l1_ratio=.5, 
                                init='nndsvd')

        def dummy_fun(self, doc):
                return doc

        def fit_data(self):
                '''
                        fit_data
                        :param no_params: no params
                        :return nmf.fit: nmf fitted
                        :rtype: object
                '''
                # Fitter sur les données
                return self.nmf.fit(self.tfidf)

        def get_topics(self):
                '''
                        get_topics
                        :param no_params: no params
                        :return topics_list: List of topics
                        :rtype: list of tuples
                '''
                feature_names = self.tfidf_vectorizer.get_feature_names()
                topics_list = []
                for topic_idx, topic in enumerate(self.nmf.components_):
                        top_words_list = [feature_names[i] for i in topic.argsort()[:-self.nb_top_words - 1:-1]]
                        # top_words_string = " ".join(top_words_list)
                        item_tp = (topic_idx, top_words_list)
                        topics_list.append(item_tp)                        
                return topics_list