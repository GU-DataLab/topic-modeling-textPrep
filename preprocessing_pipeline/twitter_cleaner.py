
class TwitterCleaner:
    def remove_rt(self, d):
        new_d = []
        for w in d:
            if len(w) > 0 and w.lower() != 'rt':
                new_d.append(w)
        return new_d

    def batch_remove_rt(self, D):
        return [self.remove_rt(d) for d in D]

    def remove_hashtags(self, d):
        new_d = []
        for w in d:
            if len(w) > 0 and w[0] != '#':
                new_d.append(w)
        return new_d

    def batch_remove_hashtags(self, D):
        return [self.remove_hashtags(d) for d in D]

    def remove_users(self, d):
        new_d = []
        for w in d:
            if len(w) > 0 and w[0] != '@':
                new_d.append(w)
        return new_d

    def batch_remove_users(self, D):
        return [self.remove_users(d) for d in D]

    def batch_remove_retweets(self, D):
        new_D = []
        for d in D:
            if len(d) > 0 and d[0].lower() != 'rt':
                new_D.append(d)
        return D

    def remove_deleted_tweets(self, d):
        if ' '.join(d) == 'This tweet has been removed in accordance with Twitter\'s policy. ' \
                          'Twitter requires all its partners to remove tweets from their systems as ' \
                          'soon as they are deleted on Twitter itself.':
            return []
        return d

    def batch_remove_deleted_tweets(self, D):
        new_D = []
        for d in D:
            d = self.remove_deleted_tweets(d)
            if len(d) > 0:
                new_D.append(d)
        return D

    def __str__(self):
        return 'Twtr'
