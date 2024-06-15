from USML.instructions import instruction
from USML.bitString import BitString

class Halt(instruction.Instruction):
    name = "Halt"
    mnemonic = "HLT"
    expectedParams = []
    
    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        return "END"

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["HLT"]],
            [
                [".Halt"],
                ["JMP", "Halt"]
            ]
        ]