# textPrep
a text preprocessing library for topic models

### Requirements
to install relevant requirements:
> pip install -r requirements.txt

Additional NLTK packages needed:
> stopwords
> 
> wordnet
> 
> averaged_perceptron_tagger

To install NLTK packages:
> python
```python
import nltk 
nltk.download()
```

Choose just the required packages (the whole set of additional NLTK data is massive)

### Using textPrep

#### Creating a pipeline and preprocessing
```python
from preprocessing_pipeline import (Preprocess, RemovePunctuation, Capitalization, RemoveStopWords, RemoveShortWords, TwitterCleaner, RemoveUrls)

# initialize the pipeline
pipeline = Preprocess()

# initialize the rules you want to use
rp = RemovePunctuation(keep_hashtags=False)
ru = RemoveUrls()
cap = Capitalization()

# include extra data in a rule if necessary
from nltk.corpus import stopwords
stopwords_list = stopwords.words('english')
stopwords_list.append(['rt', 'amp'])

rsw = RemoveStopWords(extra_sw=stopwords_list)

# add rules to the pipeline (the stringified rule makes it easy to save the pipeline details)
pipeline.document_methods = [(ru.remove_urls, str(ru),),
                             (rp.remove_punctuation, str(rp),),
                             (cap.lowercase, str(cap),),
                             (rsw.remove_stopwords, str(rsw),)
                             ]
```

You can load your data however you want, so long as it ends up as a list of lists. We provide methods for loading CSV files with and without dates.
```python
# load the data
def load_dataset_with_dates(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(line.strip().split('\t')[1].split(' '))
    return dataset

dataset = load_dataset_with_dates('data/sample_tweets.csv')
# dataset[i] = ['list', 'of', 'words', 'in', 'document_i']

# initialize the pipeline runner
from preprocessing_pipeline.NextGen import NextGen

runner = NextGen()

# preprocess the data, with some extra ngrams thrown in to ensure they are considered regardless of frequency
processed_dataset = runner.full_preprocess(dataset, pipeline, ngram_min_freq=10, extra_bigrams=None, extra_ngrams=['donald$trump', 'joe$biden', 'new$york$city'])

# assess data quality quickly and easily
from evaluation_metrics.dataset_stats import get_data_stats
print(get_data_stats(processed_dataset))
```

You can do some extra filtering after preprocessing, like TF-IDF filtering
```python
from settings.common import word_tf_df

freq = {}
freq = word_tf_df(freq, processed_dataset)
filtered_dataset = runner.filter_by_tfidf(dataset=processed_dataset, freq=freq, threshold=0.25)

# assess data quality again 
from evaluation_metrics.dataset_stats import get_data_stats
print(get_data_stats(filtered_dataset))
```