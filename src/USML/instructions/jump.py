from USML.instructions import instruction
from USML.bitString import BitString

class Jump(instruction.Instruction):
    name = "Jump"
    mnemonic = "JMP"
    description = "Jumps to the label."
    expectedDataType = ["label"]
    usageTypes = ["in"]
    tags = ["force jump"]

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        return memory[params[0]]["value"]

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["JMP", "PARAM1"]],
            [
                ["SET", "one", "1"],
                ["JMIF", "PARAM1", "one"]
            ],
            [
                ["RST", "zero"],
                ["JMIFN", "PARAM1", "zero"]
            ]
        ]