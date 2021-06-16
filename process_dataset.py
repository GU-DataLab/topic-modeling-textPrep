from settings.common import word_tf_df
from preprocessing_pipeline.NextGen import NextGen


def load_flat_dataset(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(line.strip().split(' '))
    return dataset


def load_dataset_with_dates(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(line.strip().split('\t')[1].split(' '))
    return dataset


if __name__ == '__main__':
    dataset_names = ['twitter']
    forbidden_words = []
    syn_file = None
    extra_ngrams = []

    for j in range(0, len(dataset_names)):
        ds = dataset_names[j]
        print(ds)

        ng = NextGen()
        path = 'data/{}_heavyweight.csv'.format(ds)
        dataset = load_flat_dataset(path)
        freq = {}
        freq = word_tf_df(freq, dataset)
        print(len(dataset))
        processed_dataset = ng.filter_by_tfidf(dataset=dataset, freq=freq, threshold=0.25)

        with open('data/{}_crazy4.csv'.format(ds), 'w') as f:
            for i in range(0, len(processed_dataset)):
                doc = processed_dataset[i]
                f.write('{}\n'.format(' '.join(doc)))
