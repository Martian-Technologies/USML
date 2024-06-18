from USML.instructions import instruction
from USML.bitString import BitString

class Jump(instruction.Instruction):
    name = "Jump"
    mnemonic = "JMP"
    expectedDataType = ["label"]
    usageTypes = [None]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        return memory[params[0]]["value"]

    def getImplementations(self) -> list[list[list[str]]]:
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