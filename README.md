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

# initialize the pipeline runner
from preprocessing_pipeline.NextGen import NextGen

runner = NextGen()

# load the data
def load_dataset_with_dates(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(line.strip().split('\t')[1].split(' '))
    return dataset

dataset = load_dataset_with_dates('data/sample_tweets.csv')

# preprocess the data
processed_dataset = runner.full_preprocess(dataset, pipeline, ngram_min_freq=10)
```

You can do some extra filtering after preprocessing, like TF-IDF filtering
```python
from settings.common import word_tf_df

freq = {}
freq = word_tf_df(freq, processed_dataset)
filtered_dataset = runner.filter_by_tfidf(dataset=processed_dataset, freq=freq, threshold=0.25)
```