from gensim.models.phrases import Phrases, Phraser

# DEPRECATED
class NGram:
    '''
    TRIGRAMS DEPRECATED
    gets bigrams and trigrams. notice bigram is a phraser and trigram is a phrases. phraser is smaller and faster
    than phrases, but cannot be updated. we update trigram but not bigram.
    '''
    def get_batch_phrases_old(self, documents):
        phrases = Phrases(documents, min_count=1, threshold=0.1)
        self.bigram = Phraser(phrases)
        self.trigram = Phrases(self.bigram[documents], min_count=1, threshold=0.1)
        trigrams = self.trigram[documents]
        return list(trigrams)

    def get_batch_phrases(self, documents):
        phrases = Phrases(documents, min_count=1, threshold=0.1)
        self.bigram = Phraser(phrases)
        bigrams = self.bigram[documents]
        return list(bigrams)

    def phrase_document(self, d):
        b = self.bigram[d]
        self.trigram.add_vocab(b)
        return list(self.trigram[b])

    def __str__(self):
        return 'NGrams'
