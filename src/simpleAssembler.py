import json

from USML.contextDataGetter import ContextDataGetter
from USML.baseAssembler import Assembler

class SimpleAssembler(Assembler):
    with open("src/Costs.json") as f:
        simpleCosts:dict[str, float] = json.load(f)
    with open("src/hasInstruction.json") as f:
        instructionsToUse:dict[str, bool] = json.load(f)

    @staticmethod
    def hasInstruction(instructionName):
        if instructionName in SimpleAssembler.instructionsToUse:
            return SimpleAssembler.instructionsToUse[instructionName]
        return False
    
    @staticmethod
    def getSimpleCost(instructionName):
        if instructionName in SimpleAssembler.simpleCosts:
            return SimpleAssembler.simpleCosts[instructionName]
    
    @staticmethod
    def assemble(context):
        dataGetter = ContextDataGetter(context)
        
