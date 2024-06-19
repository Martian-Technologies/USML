from USML.instructions import instruction
from USML.bitString import BitString

class IncrementIf(instruction.Instruction):
    name =  "Increment If"
    mnemonic = "INCI"
    description = "Increments the value of variable 1 by 1 if variable 2 is 0."
    expectedDataType = ["var", "var"]
    usageTypes = ["both", "in"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        if memory[params[1]]["value"].getInt() != 0:
            memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() + 1)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["INCI", "PARAM1", "PARAM2"]]
            [
                ["JMIFN", "NoInc", "PARAM2"],
                ["INC", "PARAM1"],
                [".NoInc"]
            ]
        ]