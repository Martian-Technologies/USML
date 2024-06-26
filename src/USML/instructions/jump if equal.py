from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class JumpIfEqual(Instruction):
    name = "Jump If Equal"
    mnemonic = "JMIFE"
    description = "Jumps to the label if the values of variable 2 and variable 3 are equal."
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() == memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["EQU", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]