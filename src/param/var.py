from param.param import Param

class Var(Param):
    def __init__(self, name:str, valueRange:tuple[int, int]):
        self.name = name
        self.valueRange = valueRange
        self.currentValue = None

    def getType(self):
        return "var"

    def getName(self):
        return self.name

    def getRange(self):
        return self.valueRange

    def getCurrentValue(self):
        return self.currentValue