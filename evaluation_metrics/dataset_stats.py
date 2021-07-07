from settings.common import get_vocabulary, word_frequency
import numpy as np
from nltk.corpus import stopwords


def count_stopwords(d, stopwords):
    c = 0
    for w in d:
        if w in stopwords:
            c += 1
    return c

def get_data_stats(dataset):
    dataset_size = len(dataset)
    vocab_size = len(get_vocabulary(dataset))
    freq = {}
    freq = word_frequency(freq, dataset)
    avg_token_freq = np.mean([freq[x] for x in freq.keys()])
    doc_lengths = [len(d) for d in dataset]
    total_tokens = sum(doc_lengths)
    avg_token_per_doc = np.mean(doc_lengths)
    stopwords_list = stopwords.words('english')
    stopwords_list.extend(['rt', 'amp'])
    avg_stopwords_per_doc = np.mean([count_stopwords(d, stopwords_list) for d in dataset])
    return [dataset_size, vocab_size, total_tokens, avg_token_freq, avg_token_per_doc, avg_stopwords_per_doc]