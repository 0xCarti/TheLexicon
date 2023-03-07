class Docket:
    links = {}

    def __init__(self, links: dict = None):
        if links is None:
            links = {}
        self.links = links

    def __repr__(self):
        return self.links

