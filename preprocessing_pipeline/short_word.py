

class RemoveShortWords:
    def __init__(self, min_length=4):
        self.min_length = min_length

    def remove_short_words(self, d):
        new_d = []
        for w in d:
            if len(w) >= self.min_length:
                new_d.append(w)
        return new_d

    def batch_remove_urls(self, D):
        return [self.remove_short_words(d) for d in D]

    def __str__(self):
        return 'ShortWords'
