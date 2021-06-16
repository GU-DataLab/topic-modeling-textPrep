from nltk.tag import pos_tag


class PartOfSpeech:
    def __init__(self):
        pass

    def tag_document(self, d):
        return pos_tag(d)

    def is_pos(self, term_tuple, pos='NNP'):
        '''
        :param term:
        :param pos (http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html):
        :return:
        '''
        if term_tuple[1] == pos:
            return True
        return False

    def keep_pos(self, d, pos=('',)):
        new_d = []
        temp_d = []
        for w in d:
            if len(w) > 0:
                temp_d.append(w)
        tagged_d = self.tag_document(temp_d)
        for i in range(0, len(tagged_d)):
            w_tup = tagged_d[i]
            if w_tup[1] in pos:
                new_d.append(temp_d[i])
        return new_d

    def batch_keep_pos(self, D, pos=('',)):
        return [self.keep_pos(d, pos) for d in D]

    def __str__(self):
        return 'PoS'
