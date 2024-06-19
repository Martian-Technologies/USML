import json

from USML.contextDataGetter import ContextDataGetter


class Assembler:
    def __init__(self) -> None:
        with open("src/Costs.json") as f:
            self.simpleCosts:dict[str, float] = json.load(f)
        with open("src/hasInstruction.json") as f:
            self.instructionsToUse:dict[str, bool] = json.load(f)

    def hasInstruction(self, instructionName):
        if instructionName in self.instructionsToUse:
            return self.instructionsToUse[instructionName]
        return False
    
    def getSimpleCost(self, instructionName):
        if instructionName in self.simpleCosts:
            return self.simpleCosts[instructionName]
        
    def assemble(self, context):
        dataGetter = ContextDataGetter(context)
        
