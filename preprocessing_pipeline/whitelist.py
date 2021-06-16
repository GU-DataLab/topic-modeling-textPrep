
class Whitelist:
    def __init__(self, whitelist=None):
        if whitelist is None:
            self.whitelist = []
        else:
            self.whitelist = whitelist

    def clean_doc_by_whitelist(self, d, whitelist=None):
        if whitelist is None:
            whitelist = self.whitelist
        clean_document = []
        for term in d:
            if term in whitelist:
                clean_document.append(term)
        return clean_document

    def clean_by_whitelist(self, D, whitelist=None):
        if whitelist is None:
            whitelist = self.whitelist
        clean_dataset = []
        for d in D:
            clean_document = []
            for term in d:
                if term in whitelist:
                    clean_document.append(term)
            if len(clean_document) > 0:
                clean_dataset.append(clean_document)
        return clean_dataset

    def __str__(self):
        return 'Whitelist'
