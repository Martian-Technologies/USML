from USML.instructions import instruction
from USML.bitString import BitString

class Decrement(instruction.Instruction):
    name =  "Decrement"
    mnemonic = "DEC"
    expectedDataType = ["var"]
    usageTypes = ["both"]
    tags = []

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() - 1)

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["DEC", "PARAM1"]],
            [
                ["SET", "one", "1"],
                ["DECI", "PARAM1", "one"]
            ],
            [
                ["SET", "one", "1"],
                ["ADD", "PARAM1", "one", "PARAM1"]
            ]
        ]