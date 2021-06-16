

class Blacklist:
    def __init__(self, blacklist_words=None):
        self.blacklist_words = blacklist_words

    def remove_blacklist_words(self, d):
        '''
        also removes null words
        :param d, list of words:
        :return d, without stopwords or short words:
        '''
        new_d = []
        for i in range(0, len(d)):
            if len(d[i]) > 1:
                if d[i].lower() not in self.blacklist_words:
                    new_d.append(d[i])
        return new_d

    def batch_remove_stopwords(self, D):
        return [self.remove_blacklist_words(d) for d in D]

    def __str__(self):
        return 'Blacklist'
