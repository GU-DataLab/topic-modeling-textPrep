import re


class RemoveUrls:
    def __init__(self):
        pass

    def remove_urls(self, d):
        new_d = []
        for w in d:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', w)
            for url in urls:
                w = w.replace(url, '')
            if 'http' in w:
                w = ''
            if len(w) > 0:
                new_d.append(w)
        return new_d

    def batch_remove_urls(self, D):
        return [self.remove_urls(d) for d in D]

    def __str__(self):
        return 'URLs'
