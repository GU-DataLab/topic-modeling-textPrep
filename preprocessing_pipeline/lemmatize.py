from nltk.corpus import wordnet


class Lemmatize:
    def lemmatize(self, word, ing=True):
        '''
        Return lemmatized noun or verb, else return None
        '''
        lemmas = wordnet._morphy(word, 'n')
        if lemmas:
            return min(lemmas, key=len)
        lemmas = wordnet._morphy(word, 'a')
        if lemmas:
            return min(lemmas, key=len)
        lemmas = wordnet._morphy(word, 'v')
        if lemmas:
            return min(lemmas, key=len)
        if ing and word.endswith('in'):
            word += 'g'
            lemmas = wordnet._morphy(word, 'v')
            if lemmas:
                return min(lemmas, key=len)
        return None

    def lemmatize_document(self, d, strict=False):
        new_d = []
        for i in range(0, len(d)):
            word = d[i]
            lemmatized_word = self.lemmatize(word)
            if lemmatized_word is not None:
                new_d.append(lemmatized_word)
            elif not strict:
                new_d.append(d[i])
        return new_d

    def batch_lemmatize(self, D, strict=False):
        return [self.lemmatize_document(d, strict) for d in D]

    def __str__(self):
        return 'Lemmatization'
