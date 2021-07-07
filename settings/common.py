from datetime import datetime, timedelta
from dateutil.parser import parse
from preprocessing_pipeline import (Preprocess, RemovePunctuation, Capitalization, Stem, RemoveStopWords,
                                    RemoveShortWords, TwitterCleaner, RemoveUrls, Synonyms, Blacklist, Lemmatize)


def get_pp_pipeline(remove_stopwords=False, stem=True, lemmatize=False, stopwords=None, blacklist_words=None,
                    synonyms=False, hashtags=False, synonym_file=None, remove_urls=True, cap_norm=True,
                    remove_shortwords=True, clean_twitter=True):
    pp = Preprocess()

    rp = RemovePunctuation(keep_hashtags=hashtags)
    ru = RemoveUrls()
    cap = Capitalization()
    short_words = RemoveShortWords()
    tc = TwitterCleaner()

    pp.document_methods = []

    if clean_twitter:
        pp.document_methods = [(tc.remove_deleted_tweets, str(tc),),
                               (tc.remove_users, str(tc),),
                               (tc.remove_rt, str(tc),),
                               ]

    if remove_urls:
        pp.document_methods.append((ru.remove_urls, str(ru),))

    pp.document_methods.append((rp.remove_punctuation, str(rp),))

    if cap_norm:
        pp.document_methods.append((cap.lowercase, str(cap),))

    if blacklist_words:
        bl = Blacklist(blacklist_words)
        pp.document_methods.append((bl.remove_blacklist_words, str(bl),))

    if remove_stopwords:
        rsw = RemoveStopWords(extra_sw=stopwords)
        pp.document_methods.append((rsw.remove_stopwords, str(rsw),))

    if synonyms:
        syn = Synonyms()
        pp.document_methods.append((syn.replace_synonyms, str(syn),))

    if synonym_file:
        syn = Synonyms(file=synonym_file)
        pp.document_methods.append((syn.old_replace_synonyms, str(syn),))

    if stem:
        stemmer = Stem()
        pp.document_methods.append((stemmer.stem_document, str(stemmer),))
    elif lemmatize:
        lem = Lemmatize()
        pp.document_methods.append((lem.lemmatize_document, str(lem),))

    if remove_shortwords:
        pp.document_methods.append((short_words.remove_short_words, str(short_words),))
    return pp


def save_flat_list(l, file):
    with open(file, 'w') as f:
        f.write('\n'.join(l))


def load_flat_dataset(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(line.strip().split(' '))
    return dataset


def load_dataset_with_dates(path):
    dataset = []
    try:
        with open(path, 'r') as f:
            for line in f:
                dataset.append(line.strip().split('\t')[1].split(' '))
        return dataset
    except FileNotFoundError:
        print('The path provided for your dataset does not exist: {}'.format(path))
        import sys
        sys.exit()


def get_vocabulary(docs):
    '''
    This version of get_vocabulary takes 0.08 seconds on 100,000 documents whereas the old version took forever.
    '''
    vocab = []
    for i in range(0, len(docs)):
        vocab.extend(docs[i])
    return list(set(vocab))


def word_frequency(frequency, docs):
    '''
    :param frequency: passed explicitly so that you can increment existing frequencies if using in online mode
    :param docs:
    :return: updated frequency

    '''
    for doc in docs:
        for word in doc:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
    return frequency


def word_co_frequency(frequency, docs):
    for doc in docs:
        for i in range(0, len(doc) - 1):
            w1 = doc[i]
            for j in range(i + 1, len(doc)):
                w2 = doc[j]
                word_list = sorted([w1, w2])
                word_tup = tuple(word_list)
                if not word_tup in frequency:
                    frequency[word_tup] = 0
                frequency[word_tup] += 1
    return frequency


def word_tf_df(frequency, docs):
    '''
    :param frequency: passed explicitly so that you can increment existing frequencies if using in online mode
    :param docs:
    :return: updated frequency freq[0] = df, freq[1] = tf

    '''
    for doc in docs:
        doc_word = []
        for word in doc:
            if word not in frequency:
                frequency[word] = [0, 0]
            frequency[word][1] += 1
            if word not in doc_word:
                frequency[word][0] += 1
                doc_word.append(word)
    return frequency


def normalize_frequencies(frequencies, k):
    nf = {}
    for key in frequencies.keys():
        nf[key] = frequencies[key] / k
    return nf


def save_topics(topics, path):
    with open(path, 'w') as f:
        for topic in topics:
            f.write('{}\n'.format(','.join(topic)))


def save_noise_dist(noise, path):
    with open(path, 'w') as f:
        for word, freq in noise:
            f.write('{},{}\n'.format(word, freq))


def load_topics(path):
    topics = []
    with open(path, 'r') as f:
        for line in f:
            words = line.strip().split(',')
            for i in range(0, len(words)):
                words[i] = words[i].strip().replace(' ', '$')
            words = [w for w in words if len(w) > 0]
            topics.append(words)
    return topics


def load_noise_words(path):
    noise_words = []
    with open(path, 'r') as f:
        for line in f:
            word = line.strip()
            noise_words.append(word)
    return noise_words
