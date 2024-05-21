from pram.pram import Pram

class Num(Pram):
    def __init__(self, value:int):
        self.value = value

    def getType(self):
        return "num"

    def getValue(self):
        return self.value