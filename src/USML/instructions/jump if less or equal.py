from USML.instructions import instruction
from USML.bitString import BitString

class JumpIfLessOrEqual(instruction.Instruction):
    name = "Jump If Less Or Equal"
    mnemonic = "JMIFLE"
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() <= memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["JMIFLE", "PARAM1", "PARAM2", "PARAM3"]],
            [["JMIFGE", "PARAM1", "PARAM3", "PARAM2"]],
            [
                ["LOE", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]