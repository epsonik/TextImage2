from Language import Language


class Rule(Language):
    def __init__(self, name='', id=0, psal=0, id_first=0, id_second=0, operator='', textPL='', textENG=''):
        super().__init__(textPL, textENG)
        self.name = name
        self.id = id
        # istotnosc
        self.psal = psal
        self.id_first = id_first
        self.id_second = id_second
        self.operator = operator
