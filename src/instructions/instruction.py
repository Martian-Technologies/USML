from __future__ import annotations

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    
    def __init__(self):
        pass

    @staticmethod
    def getCostIfAdded(instructionName, context):
        return lookUp.getCost(instructionName)

import lookUp