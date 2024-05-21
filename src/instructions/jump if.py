from pram.pram import Pram
from instructions import instruction

class JumpIf(instruction.Instruction):
    name = "Jump If"
    mnemonic = "JMIF"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["JMIF", "PRAM1", "PRAM2"]],
            [
                ["JMIFN", "DontDoJump", "PRAM2"],
                ["JMP", "PRAM1"],
                [".DontDoJump"]
            ]
        ]