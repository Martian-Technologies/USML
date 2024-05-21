from pram.pram import Pram
from instructions import instruction

class BitShiftLeftWithOverflow(instruction.Instruction):
    name = "Bit Shift Left With Overflow"
    mnemonic = "BSLO"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["BSLO", "PRAM1", "PRAM2", "PRAM3"]],
            [
                ["RST", "zero"],
                ["BSROF", "PRAM1", "PRAM2", "PRAM3", "zero"]
            ]
        ]