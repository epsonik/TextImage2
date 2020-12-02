from Language import Language


class Prop(Language):
    def __init__(self, name='', id=0, psal=0, farg=0, ftype=0, fthr=0, textPL='', textENG=''):
        super().__init__(textPL, textENG)
        self.name = name
        self.id = id
        self.psal = psal
        self.farg = farg
        self.ftype = ftype
        self.fthr = fthr
