from USML.instructions import instruction
from USML.bitString import BitString

class JumpIfNot(instruction.Instruction):
    name = "Jump If Not"
    mnemonic = "JMIFN"
    expectedDataType = ["label", "var"]
    usageTypes = ["in", "in"]
    tags = ["maybe jump"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() == 0:
            return memory[params[0]]["value"]

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["JMIFN", "PARAM1", "PARAM2"]],
            [
                ["JMIF", "DontDoJump", "PARAM2"],
                ["JMP", "PARAM1"],
                [".DontDoJump"]
            ]
        ]