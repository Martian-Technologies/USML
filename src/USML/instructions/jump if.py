from USML.instructions import instruction
from USML.bitString import BitString

class JumpIf(instruction.Instruction):
    name = "Jump If"
    mnemonic = "JMIF"
    expectedParams = ["label", 'var']
    
    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() != 0:
            return memory[params[0]]["value"]

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["JMIF", "PARAM1", "PARAM2"]],
            [
                ["JMIFN", "DontDoJump", "PARAM2"],
                ["JMP", "PARAM1"],
                [".DontDoJump"]
            ]
        ]