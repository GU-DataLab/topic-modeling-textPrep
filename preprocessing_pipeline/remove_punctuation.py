from string import punctuation
import re


class RemovePunctuation:
    punc = punctuation
    large_punc = ['&amp;']

    def __init__(self, is_twitter=True, keep_hashtags=True):
        self.r = r'[^\w\s]'
        if is_twitter and keep_hashtags:
            self.punc = punctuation.replace('@', '')
            self.r = r'[^\w\s#@]'
        elif is_twitter:
            self.punc = punctuation.replace('#', '')
            self.r = r'[^\w\s@]'
        elif keep_hashtags:
            self.r = r'[^\w\s#]'

    def remove_punctuation(self, d):
        new_d = []
        for w in d:
            w = re.sub(self.r, "", w)
            if len(w) > 0:
                new_d.append(w)
        return new_d

    def remove_punctuation_deprecated(self, d):
        new_d = []
        for w in d:
            for p in self.large_punc:
                w = w.replace(p, '')
            new_w = w.translate(w.maketrans('', '', self.punc))
            if len(new_w) > 0:
                new_d.append(new_w)
        return new_d

    def batch_remove_punctuation(self, D):
        return [self.remove_punctuation(d) for d in D]

    def __str__(self):
        return 'Punctuation'
