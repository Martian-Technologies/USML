from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class JumpIfNot(Instruction):
    name = "Jump If Not"
    mnemonic = "JMIFN"
    description = "Jumps to the label if the value of variable 2 is 0."
    expectedDataType = ["label", "var"]
    usageTypes = ["in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() == 0:
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFN", "PARAM1", "PARAM2"]],
            [
                ["JMIF", "DontDoJump", "PARAM2"],
                ["JMP", "PARAM1"],
                [".DontDoJump"]
            ]
        ]