from __future__ import annotations

class Instruction:
    name = "Defalt"
    mnemonic = "Defalt"
    
    def __init__(self):
        pass

    @staticmethod
    def getCostIfAdded(instructionName, context):
        """
        gets the cost if this instruction is added in this contex
        """
        return lookUp.getCost(instructionName)

import lookUp