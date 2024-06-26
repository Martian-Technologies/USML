from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Decrement(Instruction):
    name =  "Decrement"
    mnemonic = "DEC"
    description = "Decrements the value of variable 1 by 1."
    expectedDataType = ["var"]
    usageTypes = ["both"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() - 1)

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
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