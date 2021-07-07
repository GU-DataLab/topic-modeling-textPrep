from preprocessing_pipeline import Preprocess, whitelist, TFIDF
from settings import ngrams
from settings.common import word_frequency


# given a data set in form list of documents (d = [w1, w2, ... w_k])
# preprocess according to some pipeline
# get the frequency counts
# get the optimal window
# preprocess again using a whitelist with the terms in the window
# run model

class NextGen:

    def __init__(self, dataset=None, pp=None):
        self.dataset = dataset
        self.pp = pp

    def _preprocess_dataset(self, dataset, pp):
        if not dataset:
            raise ValueError('Dataset cannot be None.')
        if not pp:
            raise ValueError('Preprocessor cannot be None.')

        cleaned_dataset = []
        for i in range(0, len(dataset)):
            d = dataset[i]
            d = pp.clean_document(d)
            if len(d) > 0:
                cleaned_dataset.append(d)
        return cleaned_dataset

    def preprocess_initial_dataset(self, dataset=None, pp=None, ngram_min_freq=256, extra_bigrams=None,
                                   extra_ngrams=None):
        if not dataset:
            dataset = self.dataset
        if not pp:
            pp = self.pp

        dataset = self._preprocess_dataset(dataset, pp)
        if ngram_min_freq > 0:
            dataset = ngrams.insert_ngrams_flat(dataset, min_freq=ngram_min_freq, extra_bigrams=extra_bigrams,
                                                extra_ngrams=extra_ngrams)

        self.dataset = dataset
        return dataset

    def compute_frequencies(self, dataset=None):
        if not dataset:
            dataset = self.dataset
        frequency_dict = {}
        frequency_dict = word_frequency(frequency_dict, dataset)
        return frequency_dict

    def get_window_params(self, frequency_dict):
        min_freq = 1
        max_freq = len(self.dataset)
        return min_freq, max_freq

    def get_whitelist_from_window(self, frequency_dict, min_freq, max_freq):
        wl = []
        for k in frequency_dict.keys():
            v = frequency_dict[k]
            if v >= min_freq and v <= max_freq:
                wl.append(k)
        return wl

    def preprocess_whitelist(self, wl, dataset=None):
        if not dataset:
            dataset = self.dataset
        if not dataset:
            raise ValueError('Dataset cannot be None. Dataset: {}'.format(type(dataset)))
        if not type(wl) == type([]):
            raise ValueError('Whitelist must be a list. WL Type: {}'.format(type(wl)))

        pp = Preprocess()
        wl_class = whitelist.Whitelist(whitelist=wl)
        pp.document_methods = [(wl_class.clean_doc_by_whitelist, str(wl_class),)]

        dataset = self._preprocess_dataset(dataset, pp)

        self.dataset = dataset
        return dataset

    def full_preprocess(self, dataset=None, pp=None, ngram_min_freq=256, extra_bigrams=None, extra_ngrams=None, min_freq=0, max_freq=-1):
        if not dataset:
            dataset = self.dataset
        if not pp:
            pp = self.pp

        dataset = self.preprocess_initial_dataset(dataset=dataset, pp=pp, ngram_min_freq=ngram_min_freq,
                                                  extra_bigrams=extra_bigrams, extra_ngrams=extra_ngrams)
        if min_freq > 1 or max_freq > 0:
            freq = self.compute_frequencies(dataset=dataset)
            if min_freq <= 1:
                min_freq = 0
            if max_freq <= 0:
                max_freq = len(dataset) + 1
            wl = self.get_whitelist_from_window(frequency_dict=freq, min_freq=min_freq, max_freq=max_freq)
            dataset = self.preprocess_whitelist(wl=wl, dataset=dataset)

        self.dataset = dataset
        return dataset

    def filter_by_frequency(self, dataset=None, min_freq=0, max_freq=-1):
        freq = self.compute_frequencies(dataset=dataset)
        if min_freq > 1 or max_freq > 0:
            if min_freq <= 1:
                min_freq = 0
            if max_freq <= 0:
                max_freq = len(dataset) + 1
            wl = self.get_whitelist_from_window(frequency_dict=freq, min_freq=min_freq, max_freq=max_freq)
            dataset = self.preprocess_whitelist(wl=wl, dataset=dataset)
        return dataset

    def filter_by_tfidf(self, dataset=None, freq=None, threshold=0.1):
        if not dataset:
            dataset = self.dataset
        if not freq:
            freq = self.compute_frequencies(dataset=dataset)
        tfidf = TFIDF(total_documents=len(dataset), freq=freq)
        return tfidf.clean_tf_idf(dataset, threshold=threshold)


    def model(self, tm=None):
        return
