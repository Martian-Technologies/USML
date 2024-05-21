from pram.pram import Pram

class Lable(Pram):
    def __init__(self, name:str):
        self.name = name

    def getType(self):
        return "lable"

    def getName(self):
        return self.name