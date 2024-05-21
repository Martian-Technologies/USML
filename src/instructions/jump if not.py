from pram.pram import Pram
from instructions import instruction

class JumpIfNot(instruction.Instruction):
    name = "Jump If Not"
    mnemonic = "JMIFN"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["JMIFN", "PRAM1", "PRAM2"]],
            [
                ["JMIF", "DontDoJump", "PRAM2"],
                ["JMP", "PRAM1"],
                [".DontDoJump"]
            ]
        ]