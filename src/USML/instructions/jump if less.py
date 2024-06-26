from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class JumpIfLess(Instruction):
    name = "Jump If Less"
    mnemonic = "JMIFL"
    description = "Jumps to the label if the value of variable 1 is less than the value of variable 2."
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() < memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFL", "PARAM1", "PARAM2", "PARAM3"]],
            [["JMIFG", "PARAM1", "PARAM3", "PARAM2"]],
            [
                ["LES", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]