from nltk.stem import porter


class Stem:
    ps = porter.PorterStemmer()

    def stem(self, word):
        if len(word) > 0:
            return self.ps.stem(word)
        return ''

    def stem_document(self, d):
        return [self.stem(w) for w in d]

    def batch_stem(self, D):
        return [self.stem_document(d) for d in D]

    def __str__(self):
        return 'Stem'
