from param.param import Param

class Num(Param):
    def __init__(self, value:int):
        self.value = value

    def getType(self):
        return "num"

    def getValue(self):
        return self.value