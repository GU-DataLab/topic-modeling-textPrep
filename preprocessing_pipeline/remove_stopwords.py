from nltk.corpus import stopwords


class RemoveStopWords:
    stopwords_list = []

    def __init__(self, is_news=True, extra_sw=None):
        self.stopwords_list = stopwords.words('english')
        if is_news:
            self.stopwords_list.extend(['rt', '...', 'usatoday', 'usa today', 'washington post', 'washingtonpost',
                                        'commentemailshare', '</br>', 'you\'re', 'commentary', 'opinions', 'please',
                                        'news'])
        if extra_sw:
            self.stopwords_list.extend(extra_sw)

    def remove_stopwords(self, d):
        '''
        also removes null words
        :param d, list of words:
        :return d, without stopwords or short words:
        '''
        new_d = []
        for i in range(0, len(d)):
            if len(d[i]) > 1:
                if d[i].lower() not in self.stopwords_list:
                    new_d.append(d[i])
        return new_d

    def batch_remove_stopwords(self, D):
        return [self.remove_stopwords(d) for d in D]

    def __str__(self):
        return 'Stopwords'
