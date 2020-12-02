class Language:
    def __init__(self, textPL='', textENG=''):
        self.textENG = textENG
        self.textPL = textPL

    @property
    def text(self):
        from InputData import language
        if language is "PL":
            return self.textPL
        elif language is "ENG":
            return self.textENG
