
class Capitalization:
    def lowercase(self, d):
        return [w.lower() for w in d]

    def batch_lowercase(self, D):
        return [self.lowercase(d) for d in D]

    def __str__(self):
        return 'Capitalization'