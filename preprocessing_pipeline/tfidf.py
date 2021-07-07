import math


class TFIDF:
    def __init__(self, total_documents=0, freq=None):
        self.total_documents = total_documents
        if freq is not None:
            self.freq = freq
        self.min_tf_idf = 2**31
        self.max_tf_idf = -1

    def tf_idf(self, term):
        tf = self.freq[term][1]
        df = self.freq[term][0]
        if df == 0:
            df = 1
        N = self.total_documents
        test_tfidf = tf / math.log(N / df)
        if test_tfidf < self.min_tf_idf:
            self.min_tf_idf = test_tfidf
        if test_tfidf > self.max_tf_idf:
            self.max_tf_idf = test_tfidf
        return tf / math.log( N /df)

    def clean_tf_idf(self, D, threshold, total_documents=None, freq=None):
        if total_documents is not None:
            self.total_documents = total_documents
        if freq is not None:
            self.freq = freq
        clean_dataset = []
        for d in D:
            clean_document = []
            for term in d:
                if self.tf_idf(term) > threshold:
                    clean_document.append(term)
            # if len(clean_document) > 0:
            #     clean_dataset.append(clean_document)
            clean_dataset.append(clean_document)
        # print(self.min_tf_idf, self.max_tf_idf)
        return clean_dataset

    def clean_max_df(self, D, threshold, total_documents=None, freq=None):
        if total_documents is not None:
            self.total_documents = total_documents
        if freq is not None:
            self.freq = freq
        clean_dataset = []
        for d in D:
            clean_document = []
            for term in d:
                if self.freq[term][0]/self.total_documents < threshold:
                    clean_document.append(term)
            # if len(clean_document) > 0:
            #     clean_dataset.append(clean_document)
            clean_dataset.append(clean_document)
        return clean_dataset

    def clean_min_df(self, D, threshold, total_documents=None, freq=None):
        if total_documents is not None:
            self.total_documents = total_documents
        if freq is not None:
            self.freq = freq
        clean_dataset = []
        for d in D:
            clean_document = []
            for term in d:
                if self.freq[term][0] > threshold:
                    clean_document.append(term)
            # if len(clean_document) > 0:
            #     clean_dataset.append(clean_document)
            clean_dataset.append(clean_document)
        return clean_dataset

    def __str__(self):
        return 'TFIDF'
