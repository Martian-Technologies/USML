from USML.instructions import instruction
from USML.bitString import BitString

class DecrementIf(instruction.Instruction):
    name =  "Decrement If"
    mnemonic = "DECI"
    expectedDataType = ["var", "var"]
    usageTypes = ["both", "in"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() != 0:
            memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() - 1)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return[
            [["DECI", "PARAM1", "PARAM2"]],
            [
                ["JMIFN", "NoDec", "PARAM2"],
                ["INC", "PARAM1"],
                [".NoDec"]
            ]
        ]