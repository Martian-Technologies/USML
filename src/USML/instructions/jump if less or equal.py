from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class JumpIfLessOrEqual(Instruction):
    name = "Jump If Less Or Equal"
    mnemonic = "JMIFLE"
    description = "Jumps to the label if the value of variable 1 is less than or equal to the value of variable 2."
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() <= memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFLE", "PARAM1", "PARAM2", "PARAM3"]],
            [["JMIFGE", "PARAM1", "PARAM3", "PARAM2"]],
            [
                ["LOE", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]