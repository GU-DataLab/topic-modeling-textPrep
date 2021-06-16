import re
from nltk.corpus import wordnet


class Synonyms:
    synonym_to_dict = {}
    synonyms = []
    accepted_synonyms = []

    def __init__(self, file=None, strict=True):
        if file:
            self.old_load_synonyms(file)
            print(self.synonyms)


    def replace_synonyms(self, d):
        new_d = []
        for w in d:
            if w in self.synonym_to_dict:
                new_d.append(self.synonym_to_dict[w])
            else:
                new_d.append(w)
                self.synonym_to_dict[w] = w
                for syn in wordnet.synsets(w):
                    for l in syn.lemmas():
                        w2 = l.name().lower().replace('_', '$')
                        if not w2 in self.synonym_to_dict:
                            self.synonym_to_dict[w2] = w
        return new_d


    def old_load_synonyms(self, file):
        '''
        synonyms are saved in list form, because the list is very short. if this list grows by orders of magnitude,
        consider storing the synonyms in a hash table
        '''

        synonyms = []
        with open(file, 'r') as f:
            for l in f:
                words = l.strip().split(',')
                words = [w for w in words if len(w) > 0]
                synonyms.append(words)
        self.synonyms = synonyms


    def old_replace_synonyms(self, d):
        '''
        This is carefully constructed to preserve uppercase and lowercase letters for POS tagging.
        http://stackoverflow.com/a/919067
        '''
        new_d = []
        for w in d:
            found_synonym = False
            for synonym_list in self.synonyms:
                if w in synonym_list:
                    new_d.append(synonym_list[0])
                    found_synonym = True
                    break
            if not found_synonym:
                new_d.append(w)

        return new_d


    def old_batch_replace_synonyms(self, D, file=None):
        if file:
            self.old_load_synonyms(file)
        return [self.replace_synonyms(d) for d in D]


    def __str__(self):
        return 'Synonyms'
