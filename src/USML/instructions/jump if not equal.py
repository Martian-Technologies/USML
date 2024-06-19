from USML.instructions import instruction
from USML.bitString import BitString

class JumpIfNotEqual(instruction.Instruction):
    name = "Jump If Not Equal"
    mnemonic = "JMIFNE"
    expectedDataType = ["label", "var", "var"]
    usageTypes = ["in", "in", "in"]
    tags = ["maybe jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() != memory[params[2]]["value"].getInt():
            return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMIFNE", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["NEQU", "PARAM2", "PARAM3", "doJump"],
                ["JMIF", "PARAM1", "doJump"]
            ]
        ]