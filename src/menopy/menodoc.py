from menopy.token import Token


class MeNoDoc:

    name: str
    ms: str
    tokens: list[Token]
    lemmatized: bool
    diplomatic: bool
    normalized: bool
    facsimile: bool
    msa: bool

    def __init__(self, name: str, manuscript: str, lemmatized: bool, diplomatic: bool, normalized: bool, facsimile: bool, msa: bool) -> None:
        self.name = name
        self.ms = manuscript
        self.tokens: list[Token] = []
        self.lemmatized = lemmatized
        self.diplomatic = diplomatic
        self.normalized = normalized
        self.facsimile = facsimile
        self.msa = msa
    
    def add_token(self, newtoken: Token):
        self.tokens.append(newtoken)
    
    def get_full_text(self, level: str) -> str:
        full_text = ""
        for token in self.tokens:
            if level == "diplomatic":
                full_text += token.diplomatic + " "
            elif level == "normalized":
                full_text += token.normalized + " "
            elif level == "facsimile":
                full_text += token.facsimile + " "
            elif level == "lemma":
                full_text += token.lemma + " "
        return full_text