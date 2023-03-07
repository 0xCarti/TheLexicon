class Lexicon:
    definitions = {}

    def __init__(self, definitions=None):
        if definitions is None:
            definitions = {}
        self.definitions = definitions

    def add(self, word: str, definition: str):
        self.definitions[word] = definition

    def remove(self, word: str):
        self.definitions.pop(word)

    def __repr__(self):
        return self.definitions