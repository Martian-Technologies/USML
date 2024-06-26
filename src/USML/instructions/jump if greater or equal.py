from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class JumpIfGreaterOrEqual(Instruction):
    name = "Jump If Greater Or Equal"
    mnemonic = "JMIFGE"
    description = "Jumps to the label if the value of variable 1 is greater than or equal to the value of variable 2."
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() >= memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFGE", "PARAM1", "PARAM2", "PARAM3"]],
            [["JMIFLE", "PARAM1", "PARAM3", "PARAM2"]],
            [
                ["GOE", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]