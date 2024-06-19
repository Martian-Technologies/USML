from USML.instructions import instruction
from USML.bitString import BitString

class JumpIfGreater(instruction.Instruction):
    name = "Jump If Greater"
    mnemonic = "JMIFG"
    description = "Jumps to the label if the value of variable 1 is greater than the value of variable 2."
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() > memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFG", "PARAM1", "PARAM2", "PARAM3"]],
            [["JMIFL", "PARAM1", "PARAM3", "PARAM2"]],
            [
                ["GRT", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]