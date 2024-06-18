from USML.instructions import instruction
from USML.bitString import BitString

class DecrementIf(instruction.Instruction):
    name =  "Decrement If"
    mnemonic = "DECI"
    expectedDataType = ["var", "var"]
    usageTypes = ["both", "in"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() != 0:
            memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() - 1)

    def getImplementations(self) -> list[list[list[str]]]:
        return[
            [["DECI", "PARAM1", "PARAM2"]],
            [
                ["JMIFN", "NoDec", "PARAM2"],
                ["INC", "PARAM1"],
                [".NoDec"]
            ]
        ]