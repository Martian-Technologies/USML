from param.param import Param

class Label(Param):
    def __init__(self, name:str):
        self.name = name

    def getType(self):
        return "label"

    def getName(self):
        return self.name