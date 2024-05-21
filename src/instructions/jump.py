from pram.pram import Pram
from instructions import instruction

class Jump(instruction.Instruction):
    name = "Jump"
    mnemonic = "JMP"
    
    def __init__(self):
        super().__init__()

    def setPram(self, pramNumber:int, pram:Pram):
        raise Exception("Failed adding pram {pram} at {pramNumber}. Defalt instruction has no prams")

    def run(self):
        raise Exception("Failed running instruction {name}")

    def getImplementations(self):
        return [
            [["JMP", "PRAM1"]],
            [
                ["SET", "one", "1"],
                ["JMIF", "PRAM1", "one"]
            ],
            [
                ["RST", "zero"],
                ["JMIFN", "PRAM1", "zero"]
            ]
        ]