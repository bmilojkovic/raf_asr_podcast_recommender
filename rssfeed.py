
class RSSFeed():
    def __init__(self, url, tag, attribute):
        self.url = url
        self.tag = tag
        self.attribute = attribute

    def __repr__(self):
        return "url: " + self.url +", tag: " + self.tag + ", attribute: " + self.attribute